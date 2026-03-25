#!/usr/bin/env python
import urllib.request
import json

# Test des API de centres filtrés
def test_api(url, description):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            results = data.get('results', data)
            print(f"{description}: {len(results)} centres")
            for centre in results[:2]:  # Afficher les 2 premiers
                print(f"  - {centre['code']} - {centre['libelle']} ({centre['type_centre']})")
    except Exception as e:
        print(f"Erreur {description}: {e}")

print("=== TEST DES API CENTRES ===")
test_api('http://localhost:8000/api/centres-couts/?type_centre=NT_UO', 'Centres NT_UO')
test_api('http://localhost:8000/api/centres-couts/?type_centre=NT_TF&type_centre=CT_MT&type_centre=CT_CL', 'Autres centres')