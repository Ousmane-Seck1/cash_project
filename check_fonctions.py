#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cash_project.settings')
django.setup()

from analytics.models import Fonction, Hopital

print("=" * 60)
print("VÉRIFICATION DES FONCTIONS EN BASE DE DONNÉES")
print("=" * 60)

# Afficher tous les hopitaux
hopitals = Hopital.objects.all()
print(f"\nHopitaux ({hopitals.count()}):")
for h in hopitals:
    print(f"  - ID {h.id}: {h.nom} ({h.code})")

# Afficher toutes les fonctions
fonctions = Fonction.objects.all()
print(f"\nFonctions ({fonctions.count()}):")
for f in fonctions:
    print(f"  - ID {f.id}: {f.code} - {f.libelle} (hopital_id: {f.hopital_id})")

# Tester un delete
if fonctions.exists():
    f = fonctions.first()
    print(f"\n📝 Test de suppression:")
    print(f"   Suppression de Fonction ID={f.id}...")
    try:
        f.delete()
        print(f"   ✓ Suppression OK")
    except Exception as e:
        print(f"   ✗ Erreur: {e}")

print("\n" + "=" * 60)
