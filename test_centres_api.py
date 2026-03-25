#!/usr/bin/env python
import urllib.request
import json

def test_api_centres():
    try:
        url = 'http://localhost:8000/api/centres-couts/'
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            results = data.get('results', data)
            print(f"Total centres: {len(results)}")
            nt_uo = [c for c in results if c['type_centre'] == 'NT_UO']
            autres = [c for c in results if c['type_centre'] != 'NT_UO']
            print(f"Centres NT_UO: {len(nt_uo)}")
            print(f"Autres centres: {len(autres)}")
            return True
    except Exception as e:
        print(f"Erreur API: {e}")
        return False

if __name__ == "__main__":
    test_api_centres()