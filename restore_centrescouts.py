#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cash_project.settings')
django.setup()

from analytics.models import CentreCout, CentreResponsabilite, Fonction, Hopital

print("=" * 60)
print("RESTAURATION DES CENTRES DE COÛTS")
print("=" * 60)

# Vérifier les dépendances
hopital = Hopital.objects.first()
print(f"\nHopital: {hopital.nom if hopital else 'AUCUN'}")

fonctions = Fonction.objects.all()
print(f"Fonctions: {fonctions.count()}")

centres_resp = CentreResponsabilite.objects.all()
print(f"Centres de responsabilité: {centres_resp.count()}")

# Créer les centres de coûts si nécessaire
if centres_resp.count() > 0:
    print("\n✓ Création des centres de coûts...")
    
    # Données de base
    donnees = [
        {'centre_resp': centres_resp.filter(code='94.2.1').first(), 'code': '94.2.1.1', 'libelle': 'Biochimie', 'type': 'NT_UO'},
        {'centre_resp': centres_resp.filter(code='94.2.1').first(), 'code': '94.2.1.2', 'libelle': 'Parasitologie', 'type': 'NT_UO'},
        {'centre_resp': centres_resp.filter(code='94.3.1').first(), 'code': '94.3.1.1', 'libelle': 'Consultation cardio', 'type': 'CT_CL'},
        {'centre_resp': centres_resp.filter(code='94.3.1').first(), 'code': '94.3.1.2', 'libelle': 'Hospitalisation cardio', 'type': 'CT_CL'},
    ]
    
    for data in donnees:
        if data['centre_resp']:
            c, created = CentreCout.objects.get_or_create(
                code=data['code'],
                defaults={
                    'libelle': data['libelle'],
                    'type_centre': data['type'],
                    'centre_responsabilite': data['centre_resp'],
                    'est_actif': True
                }
            )
            status = "créé" if created else "existait"
            print(f"  - {c.code}: {status}")

# Vérifier le résultat
centres = CentreCout.objects.all()
print(f"\nRésultat: {centres.count()} centres de coûts")
for c in centres:
    print(f"  - ID {c.id}: {c.code} - {c.libelle}")
