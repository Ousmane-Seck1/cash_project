#!/usr/bin/env python
"""Script manuel pour vérifier les contraintes de gestion d'exercices.

Important: ce fichier ne doit pas exécuter de code à l'import,
sinon la découverte des tests CI échoue.
"""

import json
import os


def main():
    import django

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cash_project.settings')
    django.setup()

    from django.contrib.auth.models import User
    from django.test import Client

    from analytics.models import Exercice, Hopital

    print('=' * 80)
    print("TEST: Contraintes de gestion d'exercices comptables")
    print('=' * 80)

    print('\n1) PREPARATION')
    hopital = Hopital.objects.first()
    user = User.objects.filter(username='thies_test_user').first()

    if not hopital:
        print('Pas de hopital trouve')
        return 1
    if not user:
        print('User thies_test_user non trouve')
        return 1

    print(f'   Hopital: {hopital.nom}')
    print(f'   User: {user.username}')

    client = Client()
    client.login(username='thies_test_user', password='Test1234!')

    response = client.get('/api/exercices/')
    print(f'\n2) LISTE EXERCICES status={response.status_code}')

    payload = {
        'hopital': hopital.id,
        'annee': 2027,
        'date_debut': '2027-01-01',
        'date_fin': '2027-12-31',
        'est_actif': False,
        'est_clos': False,
    }
    response = client.post('/api/exercices/', data=json.dumps(payload), content_type='application/json')
    print(f'3) CREATE status={response.status_code}')

    if response.status_code == 201:
        exercice_id = response.json()['id']
        response = client.patch(
            f'/api/exercices/{exercice_id}/',
            data=json.dumps({'est_clos': True}),
            content_type='application/json',
        )
        print(f'4) CLOTURE status={response.status_code}')

        response = client.delete(f'/api/exercices/{exercice_id}/')
        print(f'5) DELETE CLOTURE status={response.status_code}')

    actif = Exercice.objects.filter(hopital=hopital, est_actif=True).first()
    if actif:
        response = client.delete(f'/api/exercices/{actif.id}/')
        print(f'6) DELETE ACTIF status={response.status_code}')

    print('\n' + '=' * 80)
    print('TEST MANUEL TERMINE')
    print('=' * 80)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
