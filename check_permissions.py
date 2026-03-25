#!/usr/bin/env python
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cash_project.settings')
django.setup()

from django.contrib.auth.models import User
from analytics.models import UserProfile, Charge, CompteCharge, CentreCout

print("=== VÉRIFICATION DES UTILISATEURS ===")
users = User.objects.all()
for user in users:
    has_profile = hasattr(user, 'profile')
    role = user.profile.role if has_profile else 'No profile'
    print(f"User: {user.username}, Profile: {role}")

print("\n=== VÉRIFICATION DES DONNÉES ===")
print(f"Comptes: {CompteCharge.objects.count()}")
print(f"Centres: {CentreCout.objects.count()}")
print(f"Charges: {Charge.objects.count()}")

print("\n=== PROFIL DE L'UTILISATEUR ADMIN ===")
try:
    admin_user = User.objects.get(username='admin')
    print(f"Admin user exists: {admin_user.username}")
    print(f"Has profile: {hasattr(admin_user, 'profile')}")
    if hasattr(admin_user, 'profile'):
        print(f"Role: {admin_user.profile.role}")
    else:
        print("Creating profile for admin...")
        profile = UserProfile.objects.create(user=admin_user, role='controleur')
        print(f"Profile created with role: {profile.role}")
except User.DoesNotExist:
    print("Admin user does not exist")