#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cash_project.settings')
django.setup()

from django.contrib.auth.models import User
from analytics.models import UserProfile

print("=" * 60)
print("UTILISATEURS ET LEURS RÔLES")
print("=" * 60)

users = User.objects.all()
for user in users:
    try:
        profile = user.profile
        role = profile.role
        print(f"✓ {user.username:20} | Rôle: {role:25} | Superuser: {user.is_superuser}")
    except UserProfile.DoesNotExist:
        print(f"✗ {user.username:20} | SANS PROFIL (pas de rôle) | Superuser: {user.is_superuser}")

print("\n" + "=" * 60)
print("Pour supprimer/modifier des données, vous devez être :")
print("  - Superuser OU")
print("  - Utilisateur avec le rôle 'controleur'")
print("=" * 60)

# Créer un utilisateur contrôleur s'il n'existe pas
if User.objects.filter(username='controleur').count() == 0:
    print("\n✓ Création d'un utilisateur contrôleur...")
    user = User.objects.create_user(username='controleur', password='controleur123')
    UserProfile.objects.create(user=user, role='controleur')
    print(f"  Username: controleur")
    print(f"  Password: controleur123")
    print(f"  Rôle: Contrôleur de Gestion")
