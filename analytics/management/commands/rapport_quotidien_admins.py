from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from analytics.models import (
    Activite,
    AuditLog,
    CentreCout,
    CompteCharge,
    Exercice,
    Fonction,
    Hopital,
    Produit,
)


class Command(BaseCommand):
    help = "Genere et envoie un rapport quotidien d'observabilite aux admins."

    def handle(self, *args, **options):
        now = timezone.now()
        since = now.replace(hour=0, minute=0, second=0, microsecond=0)

        anomalies = []
        for hopital in Hopital.objects.order_by('nom'):
            centres = CentreCout.objects.filter(centre_responsabilite__fonction__hopital=hopital)
            comptes_count = CompteCharge.objects.filter(hopital=hopital).count()

            if not Fonction.objects.filter(hopital=hopital).exists():
                anomalies.append(f"{hopital.nom}: aucune fonction configuree")
            if comptes_count == 0:
                anomalies.append(f"{hopital.nom}: aucun compte de charge configure")

            invalid_uo = centres.filter(type_centre__in=['NT_UO', 'CT_MT', 'CT_CL'], unite_oeuvre='').count()
            if invalid_uo:
                anomalies.append(f"{hopital.nom}: {invalid_uo} centre(s) avec unite d'oeuvre manquante")

            invalid_tarif = centres.filter(type_centre__in=['CT_MT', 'CT_CL'], tarif__isnull=True).count()
            if invalid_tarif:
                anomalies.append(f"{hopital.nom}: {invalid_tarif} centre(s) tarifaire(s) sans tarif")

            has_active_ex = Exercice.objects.filter(hopital=hopital, est_actif=True, est_clos=False).exists()
            if not has_active_ex:
                anomalies.append(f"{hopital.nom}: aucun exercice actif non cloture")

        missing_refs = []
        for niveau_code, niveau_label in Hopital.NIVEAU_CHOICES:
            if not Hopital.objects.filter(niveau=niveau_code, est_reference_niveau=True).exists():
                missing_refs.append(f"Pas de reference definie pour {niveau_label}")

        divergences = []
        for hopital in Hopital.objects.order_by('nom'):
            source_ref = Hopital.objects.filter(
                niveau=hopital.niveau,
                est_reference_niveau=True,
            ).exclude(id=hopital.id).first()
            if not source_ref:
                continue

            src_f = set(Fonction.objects.filter(hopital=source_ref).values_list('code', flat=True))
            tgt_f = set(Fonction.objects.filter(hopital=hopital).values_list('code', flat=True))
            src_cp = set(CompteCharge.objects.filter(hopital=source_ref).values_list('numero', flat=True))
            tgt_cp = set(CompteCharge.objects.filter(hopital=hopital).values_list('numero', flat=True))

            ecart = len(src_f - tgt_f) + len(src_cp - tgt_cp)
            if ecart > 0:
                divergences.append(
                    f"{hopital.nom} (niveau {hopital.niveau}) diverge de {source_ref.nom}: {ecart} ecart(s) detecte(s)"
                )

        failed_calculs = AuditLog.objects.filter(
            action='CALCULATE',
            description__icontains='ECHEC',
            timestamp__gte=since,
        ).count()
        audits_today = AuditLog.objects.filter(timestamp__gte=since).count()

        lines = [
            f"Rapport quotidien admins - {now.strftime('%Y-%m-%d %H:%M')}",
            "",
            f"Audits aujourd'hui: {audits_today}",
            f"Echecs de calcul aujourd'hui: {failed_calculs}",
            f"Anomalies configuration: {len(anomalies)}",
            f"References de niveau manquantes: {len(missing_refs)}",
            f"Divergences referentiel: {len(divergences)}",
            "",
            "--- Anomalies ---",
            *(['- ' + item for item in anomalies] or ['- Aucune']),
            "",
            "--- References manquantes ---",
            *(['- ' + item for item in missing_refs] or ['- Aucune']),
            "",
            "--- Divergences referentiel ---",
            *(['- ' + item for item in divergences] or ['- Aucune']),
            "",
            "--- Integrite activites/produits ---",
        ]

        for hopital in Hopital.objects.order_by('nom'):
            has_activites = Activite.objects.filter(exercice__hopital=hopital).exists()
            has_produits = Produit.objects.filter(exercice__hopital=hopital).exists()
            lines.append(
                f"- {hopital.nom}: activites={'OK' if has_activites else 'KO'}, produits={'OK' if has_produits else 'KO'}"
            )

        report = "\n".join(lines)
        self.stdout.write(report)

        recipients = list(
            User.objects.filter(is_active=True, is_superuser=True)
            .exclude(email='')
            .values_list('email', flat=True)
        )
        if not recipients:
            self.stdout.write(self.style.WARNING("Aucun email admin configuré. Rapport non envoyé par email."))
            return

        send_mail(
            subject=f"[CASH] Rapport quotidien admins - {now.strftime('%Y-%m-%d')}",
            message=report,
            from_email=None,
            recipient_list=recipients,
            fail_silently=False,
        )
        self.stdout.write(self.style.SUCCESS(f"Rapport quotidien envoyé à {len(recipients)} admin(s)."))
