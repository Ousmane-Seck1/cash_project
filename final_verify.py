#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cash_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
import json

print('=== FINAL VERIFICATION (CORRECTED) ===\n')
pwd = 'Test1234!'
checks=['thies_test_user','fatick_test_user','admin']

for uname in checks:
    u=User.objects.filter(username=uname).first()
    print('\n>>> '+uname.upper())
    if not u:
        print('NOT_FOUND')
        continue

    c=Client()

    # Test login
    if uname != 'admin':
        login_ok = c.login(username=uname, password=pwd)
        print('login_ok=', login_ok)
    else:
        c.force_login(u)
        print('login=superuser')

    def get_json(path):
        r=c.get(path)
        try:
            return json.loads(r.content.decode('utf-8'))
        except:
            return {}

    s=get_json('/api/info-session/')
    print('hospital=', s.get('hopital'), '| role=', s.get('role_code'), '| super=', s.get('is_superuser'))

    users=get_json('/api/utilisateurs/').get('results',[])
    print('users_visible=', len(users), '|', [u['username'] for u in users[:3]])

    roles=get_json('/api/hopital-roles/?est_actif=true').get('results',[])   
    print('roles_visible=', len(roles), '| hopitaux=', len(set([r.get('hopital_nom') for r in roles])))

    hops=get_json('/api/hopitaux/').get('results',[])
    print('hospitals_visible=', len(hops))

print('\n>>> SECURITY TEST: thies_user tries superuser create')
c=Client()
c.login(username='thies_test_user', password=pwd)
probe_un = 'probe_'+str(int(__import__('time').time()))
payload={
    'username': probe_un,
    'password': 'Pass1!',
    'role': 'controleur',
    'hopital_role': 1,
    'hopital': 1,
    'is_superuser': True,
    'is_active': True
}
r=c.post('/api/utilisateurs/', data=json.dumps(payload), content_type='application/json')
print('create_superuser_status=', r.status_code)
if r.status_code != 201:
    print('create_superuser_result=BLOCKED (status', r.status_code, ')')
    if r.status_code == 400:
        try:
            err = json.loads(r.content)
            print('error_detail=', err)
        except:
            pass
else:
    jdata = json.loads(r.content)
    print('create_superuser_result=VULNERABLE, is_superuser=', jdata.get('is_superuser'))
