#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cash_project.settings')
django.setup()

from analytics.models import CentreCout
from analytics.serializers import CentreCoutSerializer

print("=" * 60)
print("DIAGNOSTIC DES CENTRES DE COÛTS")
print("=" * 60)

# Afficher tous les centres
tous = CentreCout.objects.all()
print(f"\nTous les centres de coûts: {tous.count()}")
for c in tous:
    print(f"  - ID {c.id}: {c.code} - {c.libelle} (actif: {c.est_actif})")

# Afficher les actifs
actifs = CentreCout.objects.filter(est_actif=True)
print(f"\nCentres de coûts ACTIFS: {actifs.count()}")
for c in actifs:
    print(f"  - ID {c.id}: {c.code}")

# Tester la serialization
print("\nTest de serialization:")
try:
    serializer = CentreCoutSerializer(tous, many=True)
    print(f"✓ {len(serializer.data)} centres serialisés")
    for c in serializer.data[:3]:
        print(f"  - {c['code']} - {c['libelle']}")
except Exception as e:
    print(f"✗ Erreur serialization: {e}")

# Vérifier les relations
print("\nVérification des relations:")
for c in tous[:3]:
    print(f"  {c.code}: centre_responsabilite={c.centre_responsabilite}")
