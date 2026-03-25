#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cash_project.settings')
django.setup()

from analytics.models import CentreCout
from analytics.serializers import CentreCoutSerializer

print("=" * 60)
print("VÉRIFICATION DES CENTRES DE COÛTS")
print("=" * 60)

# Afficher tous les centres de coûts
centres = CentreCout.objects.all()
print(f"\nCentres de coûts en base ({centres.count()}):")
for c in centres:
    resp_code = c.centre_responsabilite.code if c.centre_responsabilite else 'NONE'
    print(f"  - ID {c.id}: {c.code} - {c.libelle} → {resp_code}")

# Tester la serialization
print("\nTest de serialization (API):")
serializer = CentreCoutSerializer(centres, many=True)
print(f"Nombre serialisés: {len(serializer.data)}")
for c in serializer.data:
    print(f"  - ID {c['id']}: {c['code']} - {c['libelle']}")
    print(f"    Centre de responsabilité: {c.get('centre_responsabilite_code', 'NONE')} - {c.get('centre_responsabilite_libelle', '')}")
