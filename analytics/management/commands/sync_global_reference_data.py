from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from analytics.models import CentreCout, CentreResponsabilite, CompteCharge, Fonction, Hopital


class Command(BaseCommand):
    help = (
        "Synchronise les referentiels globaux (fonctions, centres de responsabilite, "
        "centres de cout, comptes de charges) sur tous les hopitaux."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--source-hopital-code",
            type=str,
            help="Code de l'hopital source utilise comme referentiel maitre.",
        )
        parser.add_argument(
            "--prune",
            action="store_true",
            help="Supprime les elements non presents dans l'hopital source.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        source_code = (options.get("source_hopital_code") or "").strip()
        prune = bool(options.get("prune"))

        if source_code:
            source = Hopital.objects.filter(code=source_code).first()
            if not source:
                raise CommandError(f"Aucun hopital trouve pour le code '{source_code}'.")
        else:
            source = Hopital.objects.order_by("id").first()
            if not source:
                raise CommandError("Aucun hopital en base. Impossible de synchroniser.")

        hopitaux = list(Hopital.objects.order_by("id"))
        if len(hopitaux) < 2:
            self.stdout.write(self.style.WARNING("Un seul hopital detecte: rien a synchroniser."))
            return

        source_fonctions = list(Fonction.objects.filter(hopital=source).order_by("code"))
        source_comptes = list(CompteCharge.objects.filter(hopital=source).order_by("numero"))

        created_counts = {
            "fonctions": 0,
            "responsabilites": 0,
            "centres": 0,
            "comptes": 0,
        }
        updated_counts = {
            "fonctions": 0,
            "responsabilites": 0,
            "centres": 0,
            "comptes": 0,
        }
        deleted_counts = {
            "fonctions": 0,
            "responsabilites": 0,
            "centres": 0,
            "comptes": 0,
        }

        for hopital in hopitaux:
            if hopital.id == source.id:
                continue

            source_function_keys = {(f.code, f.libelle) for f in source_fonctions}
            source_function_codes = {f.code for f in source_fonctions}

            for src_f in source_fonctions:
                obj, created = Fonction.objects.update_or_create(
                    hopital=hopital,
                    code=src_f.code,
                    defaults={"libelle": src_f.libelle},
                )
                if created:
                    created_counts["fonctions"] += 1
                elif obj.libelle == src_f.libelle:
                    pass
                else:
                    updated_counts["fonctions"] += 1

                src_resps = list(CentreResponsabilite.objects.filter(fonction=src_f).order_by("code"))
                src_resp_codes = {r.code for r in src_resps}

                for src_r in src_resps:
                    resp_obj, resp_created = CentreResponsabilite.objects.update_or_create(
                        fonction=obj,
                        code=src_r.code,
                        defaults={"libelle": src_r.libelle},
                    )
                    if resp_created:
                        created_counts["responsabilites"] += 1
                    elif resp_obj.libelle == src_r.libelle:
                        pass
                    else:
                        updated_counts["responsabilites"] += 1

                    src_centres = list(CentreCout.objects.filter(centre_responsabilite=src_r).order_by("code"))
                    src_centre_codes = {c.code for c in src_centres}

                    for src_c in src_centres:
                        unite_oeuvre = (src_c.unite_oeuvre or "").strip()
                        if src_c.type_centre in {"NT_UO", "CT_MT", "CT_CL"} and not unite_oeuvre:
                            unite_oeuvre = "UO"

                        tarif = src_c.tarif
                        if src_c.type_centre in {"CT_MT", "CT_CL"} and tarif is None:
                            tarif = Decimal("0")

                        centre_obj, centre_created = CentreCout.objects.get_or_create(
                            centre_responsabilite=resp_obj,
                            code=src_c.code,
                            defaults={
                                "libelle": src_c.libelle,
                                "type_centre": src_c.type_centre,
                                "unite_oeuvre": unite_oeuvre,
                                "tarif": tarif,
                                "ordre_cascade": src_c.ordre_cascade,
                                "est_actif": src_c.est_actif,
                            },
                        )
                        if centre_created:
                            created_counts["centres"] += 1
                        else:
                            if centre_obj.libelle != src_c.libelle:
                                centre_obj.libelle = src_c.libelle
                                centre_obj.save(update_fields=["libelle"])
                                updated_counts["centres"] += 1

                    if prune:
                        deleted, _ = CentreCout.objects.filter(
                            centre_responsabilite=resp_obj
                        ).exclude(code__in=src_centre_codes).delete()
                        deleted_counts["centres"] += deleted

                if prune:
                    deleted, _ = CentreResponsabilite.objects.filter(
                        fonction=obj
                    ).exclude(code__in=src_resp_codes).delete()
                    deleted_counts["responsabilites"] += deleted

            for src_compte in source_comptes:
                compte_obj, compte_created = CompteCharge.objects.update_or_create(
                    hopital=hopital,
                    numero=src_compte.numero,
                    defaults={"libelle": src_compte.libelle},
                )
                if compte_created:
                    created_counts["comptes"] += 1
                elif compte_obj.libelle == src_compte.libelle:
                    pass
                else:
                    updated_counts["comptes"] += 1

            if prune:
                deleted, _ = Fonction.objects.filter(
                    hopital=hopital
                ).exclude(code__in=source_function_codes).delete()
                deleted_counts["fonctions"] += deleted

                deleted, _ = CompteCharge.objects.filter(
                    hopital=hopital
                ).exclude(numero__in=[c.numero for c in source_comptes]).delete()
                deleted_counts["comptes"] += deleted

        self.stdout.write(self.style.SUCCESS("Synchronisation terminee."))
        self.stdout.write(f"Source: {source.nom} ({source.code})")
        self.stdout.write(
            "Crees: "
            f"fonctions={created_counts['fonctions']}, "
            f"responsabilites={created_counts['responsabilites']}, "
            f"centres={created_counts['centres']}, "
            f"comptes={created_counts['comptes']}"
        )
        self.stdout.write(
            "Mis a jour: "
            f"fonctions={updated_counts['fonctions']}, "
            f"responsabilites={updated_counts['responsabilites']}, "
            f"centres={updated_counts['centres']}, "
            f"comptes={updated_counts['comptes']}"
        )
        if prune:
            self.stdout.write(
                "Supprimes: "
                f"fonctions={deleted_counts['fonctions']}, "
                f"responsabilites={deleted_counts['responsabilites']}, "
                f"centres={deleted_counts['centres']}, "
                f"comptes={deleted_counts['comptes']}"
            )
