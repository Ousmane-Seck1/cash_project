#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cash_project.settings')
django.setup()

from django.contrib.auth.models import User

# Delete probe users created during testing
probe_users = User.objects.filter(username__startswith='probe_')
count = probe_users.count()
probe_users.delete()
print(f'Deleted {count} test probe user(s)')
