#!/usr/bin/env python
"""
Script pour restaurer la configuration standard d'un hôpital
en copiant la configuration d'un hôpital de référence
"""
import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cash_project.settings')
django.setup()

from analytics.models import (
    Hopital, Fonction, CentreResponsabilite, CentreCout, 
    CompteCharge, Exercice, Charge, Activite, Produit, CleRepartition, ResultatCalcul
)
from django.db import transaction


def restore_hopital_config(hospital_name_source, hospital_name_target):
    """
    Copie la configuration d'un hôpital source vers un hôpital target.
    Supprime d'abord les données saisies de l'hôpital cible.
    
    Args:
        hospital_name_source: Nom de l'hôpital source (ex: 'Centre Hospitalier Regional de Thies')
        hospital_name_target: Nom de l'hôpital target (ex: 'Centre Hospitalier Regional de Fatick')
    """
    try:
        hopital_source = Hopital.objects.get(nom=hospital_name_source)
        hopital_target = Hopital.objects.get(nom=hospital_name_target)
    except Hopital.DoesNotExist as e:
        print(f"❌ Erreur: {e}")
        return
    
    print(f"📋 Début de restauration de {hopital_target.nom} depuis {hopital_source.nom}")
    
    with transaction.atomic():
        # 1. Supprimer les données saisies de l'hôpital cible
        print("\n🗑️  Suppression des données saisies...")
        
        # Récupérer les exercices du cible pour supprimer les données
        exercices_cible = Exercice.objects.filter(hopital=hopital_target)
        
        # Supprimer les données liées aux exercices
        for ex in exercices_cible:
            Charge.objects.filter(exercice=ex).delete()
            CleRepartition.objects.filter(exercice=ex).delete()
            Activite.objects.filter(exercice=ex).delete()
            Produit.objects.filter(exercice=ex).delete()
            ResultatCalcul.objects.filter(exercice=ex).delete()
        
        charge_count = Charge.objects.filter(exercice__hopital=hopital_target).count()
        print(f"   ✓ Charges: supprimées")
        print(f"   ✓ Clés de répartition: supprimées")
        print(f"   ✓ Activités: supprimées")
        print(f"   ✓ Produits: supprimées")
        print(f"   ✓ Résultats: supprimés")
        
        # 2. Supprimer la configuration existante du cible
        print("\n🔄 Suppression de la configuration existante...")
        CentreCout.objects.filter(centre_responsabilite__fonction__hopital=hopital_target).delete()
        CentreResponsabilite.objects.filter(fonction__hopital=hopital_target).delete()
        CompteCharge.objects.filter(hopital=hopital_target).delete()
        Fonction.objects.filter(hopital=hopital_target).delete()
        Exercice.objects.filter(hopital=hopital_target).delete()
        
        print(f"   ✓ Centres de coûts: supprimés")
        print(f"   ✓ Centres de responsabilité: supprimés")
        print(f"   ✓ Comptes de charges: supprimés")
        print(f"   ✓ Fonctions: supprimées")
        print(f"   ✓ Exercices: supprimés")
        
        # 3. Copier les Exercices
        print("\n📦 Copie de la configuration...")
        exercices_source = Exercice.objects.filter(hopital=hopital_source)
        exercice_mapping = {}
        
        for ex_src in exercices_source:
            ex_new = Exercice.objects.create(
                hopital=hopital_target,
                annee=ex_src.annee,
                date_debut=ex_src.date_debut,
                date_fin=ex_src.date_fin,
                est_actif=ex_src.est_actif,
                est_clos=ex_src.est_clos
            )
            exercice_mapping[ex_src.id] = ex_new
        print(f"   ✓ Exercices: {len(exercice_mapping)} copiés")
        
        # 4. Copier les Comptes de Charges
        compte_mapping = {}
        for compte_src in CompteCharge.objects.filter(hopital=hopital_source):
            compte_new = CompteCharge.objects.create(
                hopital=hopital_target,
                numero=compte_src.numero,
                libelle=compte_src.libelle
            )
            compte_mapping[compte_src.id] = compte_new
        print(f"   ✓ Comptes de charges: {len(compte_mapping)} copiés")
        
        # 5. Copier les Fonctions, CentreResponsabilite, CentreCout
        fonction_mapping = {}
        centre_resp_mapping = {}
        centre_cout_mapping = {}
        
        for fonction_src in Fonction.objects.filter(hopital=hopital_source):
            fonction_new = Fonction.objects.create(
                hopital=hopital_target,
                code=fonction_src.code,
                libelle=fonction_src.libelle
            )
            fonction_mapping[fonction_src.id] = fonction_new
        print(f"   ✓ Fonctions: {len(fonction_mapping)} copiées")
        
        for centre_src in CentreResponsabilite.objects.filter(fonction__hopital=hopital_source):
            centre_new = CentreResponsabilite.objects.create(
                fonction=fonction_mapping[centre_src.fonction.id],
                code=centre_src.code,
                libelle=centre_src.libelle
            )
            centre_resp_mapping[centre_src.id] = centre_new
        print(f"   ✓ Centres de responsabilité: {len(centre_resp_mapping)} copiés")
        
        for cc_src in CentreCout.objects.filter(centre_responsabilite__fonction__hopital=hopital_source):
            # Pour les centres tarifaires sans tarif, utiliser 0.00 par défaut
            tarif = cc_src.tarif
            if cc_src.type_centre in ['CT_MT', 'CT_CL'] and not tarif:
                tarif = Decimal('0.00')
            
            # Pour les centres qui demandent une unité d'oeuvre, en fournir une par défaut si manquante
            unite_oeuvre = cc_src.unite_oeuvre
            if cc_src.type_centre in ['NT_UO', 'CT_MT', 'CT_CL'] and not unite_oeuvre:
                unite_oeuvre = "Nombre d'unités"
            
            cc_new = CentreCout.objects.create(
                centre_responsabilite=centre_resp_mapping[cc_src.centre_responsabilite.id] if cc_src.centre_responsabilite else None,
                code=cc_src.code,
                libelle=cc_src.libelle,
                type_centre=cc_src.type_centre,
                unite_oeuvre=unite_oeuvre,
                tarif=tarif,
                ordre_cascade=cc_src.ordre_cascade,
                est_actif=cc_src.est_actif
            )
            centre_cout_mapping[cc_src.id] = cc_new
        print(f"   ✓ Centres de coûts: {len(centre_cout_mapping)} copiés")
        
        print("\n✅ Restauration terminée avec succès!")
        print(f"\n📊 Résumé:")
        print(f"   - Exercices: {len(exercice_mapping)}")
        print(f"   - Comptes de charges: {len(compte_mapping)}")
        print(f"   - Fonctions: {len(fonction_mapping)}")
        print(f"   - Centres de responsabilité: {len(centre_resp_mapping)}")
        print(f"   - Centres de coûts: {len(centre_cout_mapping)}")


if __name__ == '__main__':
    restore_hopital_config(
        hospital_name_source='Centre Hospitalier Regional de Thies',
        hospital_name_target='Centre Hospitalier Regional de Fatick'
    )
