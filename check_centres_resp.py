#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cash_project.settings')
django.setup()

from analytics.models import CentreResponsabilite, Fonction

print("=" * 60)
print("VÉRIFICATION DES CENTRES DE RESPONSABILITÉ")
print("=" * 60)

# Afficher toutes les fonctions
fonctions = Fonction.objects.all()
print(f"\nFonctions en base ({fonctions.count()}):")
for f in fonctions:
    print(f"  - ID {f.id}: {f.code} - {f.libelle}")

# Afficher tous les centres de responsabilité
centres_resp = CentreResponsabilite.objects.all()
print(f"\nCentres de responsabilité en base ({centres_resp.count()}):")
for c in centres_resp:
    print(f"  - ID {c.id}: {c.code} - {c.libelle} (fonction_id: {c.fonction_id})")

# Tester la serialization
print("\nTest de serialization (API):")
from analytics.serializers import CentreResponsabiliteSerializer
serializer = CentreResponsabiliteSerializer(centres_resp, many=True)
print(f"Nombre serialisés: {len(serializer.data)}")
for c in serializer.data:
    print(f"  - ID {c['id']}: {c['code']} - {c['libelle']}")

# Vérifier les foreign keys
print("\nVérification des relations:")
for c in centres_resp:
    fonction = c.fonction
    print(f"  Centre {c.code} → Fonction {fonction.code if fonction else 'NONE'}")
