#!/usr/bin/env python
import urllib.request
import urllib.error
import base64
import json

# Test de l'API avec authentification basique
url = 'http://localhost:8000/api/charges/'

# Créer l'en-tête d'authentification
credentials = base64.b64encode(b'admin:admin').decode('utf-8')
headers = {'Authorization': f'Basic {credentials}'}

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
        results = data.get('results', data)
        print(f'Status: {response.getcode()}')
        print(f'Charges trouvées: {len(results)}')
        print('API accessible !')
except urllib.error.HTTPError as e:
    print(f'Erreur HTTP: {e.code} - {e.reason}')
    print(f'Réponse: {e.read().decode("utf-8")}')
except Exception as e:
    print(f'Erreur: {e}')