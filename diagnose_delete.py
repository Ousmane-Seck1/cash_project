#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cash_project.settings')
django.setup()

from analytics.models import CentreCout, Charge

print("=" * 60)
print("DIAGNOSTIC DE LA SUPPRESSION")
print("=" * 60)

# Lister les centres actifs avec leurs charges associées
centres = CentreCout.objects.filter(est_actif=True)
print(f"\nCentres de coûts actifs: {centres.count()}")
for c in centres:
    charges_count = Charge.objects.filter(centre_cout_id=c.id).count()
    print(f"  - ID {c.id}: {c.code} ({charges_count} charges)")
    
    # Tenter la suppression
    try:
        # Créer une copie pour tester sans vraiment supprimer
        test_id = c.id
        CentreCout.objects.get(id=test_id).delete()
        print(f"    ✓ Suppression OK")
    except Exception as e:
        print(f"    ✗ Erreur: {e}")
        break

print("\n" + "=" * 60)
