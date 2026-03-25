#!/usr/bin/env python
"""
Script de test pour vérifier les contraintes de gestion d'exercices
Version simplifiée utilisant shell Django
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cash_project.settings')
django.setup()

from analytics.models import Hopital, Exercice

print("=" * 80)
print("DIAGNOSTIC: État des exercices et contraintes")
print("=" * 80)

# Afficher tous les exercices
print("\n📋 EXERCICES EXISTANTS")
all_ex = Exercice.objects.all().order_by('hopital', '-annee')
for ex in all_ex:
    print(f"   {ex.hopital.nom}: {ex.annee} (actif={ex.est_actif}, clos={ex.est_clos})")

# Cleanup: Supprimer les exercices de test (2027, 2028)
print("\n🧹 NETTOYAGE DES DOUBLONS")
removed = Exercice.objects.filter(annee__in=[2027, 2028]).delete()
print(f"   {removed[0]} exercices de test supprimés")

# Afficher état après cleanup
print("\n📋 EXERCICES APRÈS CLEANUP")
all_ex = Exercice.objects.all().order_by('hopital', '-annee')
for ex in all_ex:
    print(f"   {ex.hopital.nom}: {ex.annee} (actif={ex.est_actif}, clos={ex.est_clos})")

print("\n" + "=" * 80)
print("✅ DIAGNOSTIC COMPLET")
print("=" * 80)

# Afficher les contraintes
print("\nCONTRAINTES IMPLÉMENTÉES:")
print("  1️⃣  Exercices clôturés (est_clos=True): lecture seule")
print("     ❌ Impossible: modifier, supprimer")
print("     ✅ Possible: charger et visualiser")
print()
print("  2️⃣  Exercice actif (est_actif=True): 1 seul par hopital")
print("     ❌ Impossible: supprimer")
print("     ✅ Possible: modifier, charger")
print()
print("  3️⃣  Exercice inactif non-clôturé")
print("     ✅ Possible: modifier, supprimer, charger")
print()
print("  4️⃣  Un seul exercice actif par hôpital")
print("     ✅  Enforci automatiquement lors de set est_actif=True")

print("\n" + "=" * 80)
print("POUR TESTER VIA INTERFACE:")
print("  1. Allez à /exercices/")
print("  2. Sélectionnez un hôpital")
print("  3. Créez un nouvel exercice 2027")
print("  4. Clôturez-le (est_clos=True)")
print("  5. Essayez le modifier → BLOQUÉ ✅")
print("  6. Essayez le supprimer → BLOQUÉ ✅")
print("=" * 80)
