#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cash_project.settings')
django.setup()

from analytics.models import Hopital
from analytics.serializers import HopitalSerializer

hopitals = Hopital.objects.all()
print(f"Nombre d'hopitaux: {hopitals.count()}")
for h in hopitals:
    print(f"  - ID {h.id}: {h.nom} ({h.code})")

# Tester la serializer
if hopitals.exists():
    h = hopitals.first()
    serializer = HopitalSerializer(h)
    print(f"\nSerialization de {h.nom}: {serializer.data}")
else:
    print("\n⚠️ Aucun hopital en base! Créons-en un...")
    h = Hopital.objects.create(nom="CHU de Dakar", code="CHU-DAK")
    print(f"✓ Hopital créé: ID {h.id}")
