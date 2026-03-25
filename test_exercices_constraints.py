#!/usr/bin/env python
"""
Script de test pour vérifier les contraintes de gestion d'exercices
"""
import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cash_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from analytics.models import Hopital, Exercice
import json

print("=" * 80)
print("TEST: Contraintes de gestion d'exercices comptables")
print("=" * 80)

# Préparation
print("\n1️⃣ PRÉPARATION")
hopital = Hopital.objects.first()
user = User.objects.filter(username='thies_test_user').first()

if not hopital:
    print("❌ Pas de hopital trouvé")
    exit(1)
if not user:
    print("❌ User thies_test_user non trouvé")
    exit(1)

print(f"   Hopital: {hopital.nom}")
print(f"   User: {user.username}")

# Test 1: Lister les exercices
print("\n2️⃣ TEST: Lister les exercices")
client = Client()
client.login(username='thies_test_user', password='Test1234!')

# Vérifier le login
response = client.get('/api/info-session/')
if response.status_code != 200:
    print(f"   ❌ Login échoué: {response.status_code}")
    print(f"   Note: Utilisez force_login ou vérifiez les credentials")

response = client.get('/api/exercices/')
exercices = response.json()
print(f"   Response status: {response.status_code}")
if response.status_code == 200:
    exercices = response.json()
    print(f"   Exercices trouvés: {len(exercices.get('results', []))}")
    for ex in exercices.get('results', []):
        print(f"     - {ex['annee']}: actif={ex.get('est_actif')}, clos={ex.get('est_clos')}")
else:
    print(f"   ❌ Erreur: {response.json()}")
    print("   Utilisez force_login à la place")
    from django.test import Client as TestClient
    client = TestClient()
    client.force_login(user)

# Test 2: Créer un nouvel exercice
print("\n3️⃣ TEST: Créer un nouvel exercice")
payload = {
    'hopital': hopital.id,
    'annee': 2027,
    'date_debut': '2027-01-01',
    'date_fin': '2027-12-31',
    'est_actif': False,
    'est_clos': False
}
response = client.post('/api/exercices/', 
    data=json.dumps(payload), 
    content_type='application/json'
)
if response.status_code == 201:
    ex = response.json()
    print(f"   ✅ Exercice créé: {ex['annee']} (ID: {ex['id']})")
    exercice_id = ex['id']
else:
    print(f"   ❌ Erreur {response.status_code}: {response.json()}")

# Test 3: Modifier un exercice non-clôturé
print("\n4️⃣ TEST: Modifier un exercice non-clôturé")
payload = {
    'date_debut': '2027-01-15'  # Changer la date
}
response = client.patch(f'/api/exercices/{exercice_id}/', 
    data=json.dumps(payload), 
    content_type='application/json'
)
if response.status_code == 200:
    ex = response.json()
    print(f"   ✅ Exercice modifié: date_debut={ex['date_debut']}")
else:
    print(f"   ❌ Erreur {response.status_code}: {response.json()}")

# Test 4: Clôturer l'exercice
print("\n5️⃣ TEST: Clôturer un exercice")
payload = {
    'est_clos': True
}
response = client.patch(f'/api/exercices/{exercice_id}/', 
    data=json.dumps(payload), 
    content_type='application/json'
)
if response.status_code == 200:
    ex = response.json()
    print(f"   ✅ Exercice clôturé: est_clos={ex['est_clos']}")
else:
    print(f"   ❌ Erreur {response.status_code}: {response.json()}")

# Test 5: Essayer de modifier un exercice clôturé
print("\n6️⃣ TEST: Essayer de modifier un exercice clôturé (doit échouer)")
payload = {
    'date_debut': '2027-02-01'
}
response = client.patch(f'/api/exercices/{exercice_id}/', 
    data=json.dumps(payload), 
    content_type='application/json'
)
if response.status_code != 200:
    print(f"   ✅ Correctement bloqué: {response.json()}")
else:
    print(f"   ❌ Erreur: l'exercice clôturé a été modifié !")

# Test 6: Essayer de supprimer un exercice clôturé
print("\n7️⃣ TEST: Essayer de supprimer un exercice clôturé (doit échouer)")
response = client.delete(f'/api/exercices/{exercice_id}/', 
    headers={'X-CSRFToken': 'test'}
)
if response.status_code != 204:
    print(f"   ✅ Correctement bloqué: {response.json()}")
else:
    print(f"   ❌ Erreur: l'exercice clôturé a été supprimé !")

# Test 7: Créer et supprimer un exercice non-clôturé
print("\n8️⃣ TEST: Supprimer un exercice non-clôturé (ne doit pas être actif)")
payload = {
    'hopital': hopital.id,
    'annee': 2028,
    'date_debut': '2028-01-01',
    'date_fin': '2028-12-31',
    'est_actif': False,
    'est_clos': False
}
response = client.post('/api/exercices/', 
    data=json.dumps(payload), 
    content_type='application/json'
)
if response.status_code == 201:
    ex = response.json()
    ex_id = ex['id']
    print(f"   ✅ Exercice créé: {ex['annee']}")
    
    # Essayer de le supprimer
    response = client.delete(f'/api/exercices/{ex_id}/')
    if response.status_code == 204:
        print(f"   ✅ Exercice supprimé avec succès")
    else:
        print(f"   ❌ Erreur {response.status_code}: {response.json()}")
else:
    print(f"   ❌ Erreur création: {response.json()}")

# Test 8: Essayer de supprimer un exercice actif
print("\n9️⃣ TEST: Essayer de supprimer exercice actif (doit échouer)")
actif = Exercice.objects.filter(hopital=hopital, est_actif=True).first()
if actif:
    response = client.delete(f'/api/exercices/{actif.id}/')
    if response.status_code != 204:
        print(f"   ✅ Correctement bloqué: {response.json()}")
    else:
        print(f"   ❌ Erreur: exercice actif supprimé !")
else:
    print(f"   ⚠️  Pas d'exercice actif pour tester")

print("\n" + "=" * 80)
print("✅ TESTS TERMINÉS")
print("=" * 80)
