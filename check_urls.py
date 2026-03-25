#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cash_project.settings')
django.setup()

from django.urls import reverse, get_resolver
from analytics.views import HopitalViewSet
from rest_framework.routers import DefaultRouter

# Créer un router et enregistrer le ViewSet
router = DefaultRouter()
router.register(r'hopitaux', HopitalViewSet)

# Afficher les URLs générées
print("URLs du router:")
for url_pattern in router.urls:
    print(f"  - {url_pattern.pattern}")

# Vérifier la configuration des URLs du projet
print("\nVérification de la conf des URLs du projet:")
from django.urls import path, include
from cash_project.urls import urlpatterns

for pattern in urlpatterns:
    print(f"  - {pattern.pattern}")
