from datetime import date

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.test import TestCase
from rest_framework.test import APIClient

from analytics.models import Exercice, Hopital
from analytics.signals import provision_hospital_on_create


class WorkflowSecurityObservabilityTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        post_save.disconnect(provision_hospital_on_create, sender=Hopital)

    @classmethod
    def tearDownClass(cls):
        post_save.connect(provision_hospital_on_create, sender=Hopital)
        super().tearDownClass()

    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser('root', 'root@example.com', 'rootpass123')
        self.user = User.objects.create_user('u1', 'u1@example.com', 'pass12345')

        self.hopital = Hopital.objects.create(
            nom='Hopital Test',
            code='HTEST',
            niveau='N1',
            est_reference_niveau=True,
        )
        Exercice.objects.create(
            hopital=self.hopital,
            annee=2025,
            date_debut=date(2025, 1, 1),
            date_fin=date(2025, 12, 31),
            est_actif=True,
            est_clos=False,
        )

    def test_workflow_precheck_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.get(f'/api/exercices/workflow_annuel_precheck/?hopital={self.hopital.id}')
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn('checks', payload)
        self.assertIn('next_steps', payload)

    def test_alertes_systeme_requires_superuser(self):
        self.client.force_login(self.user)
        response = self.client.get('/api/hopitaux/alertes_systeme/')
        self.assertEqual(response.status_code, 403)

    def test_alertes_systeme_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.get('/api/hopitaux/alertes_systeme/')
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn('summary', payload)
        self.assertIn('anomalies', payload)

    def test_force_copy_requires_confirmation_code(self):
        self.client.force_login(self.superuser)
        response = self.client.post(
            f'/api/hopitaux/{self.hopital.id}/copier_referentiel_niveau/',
            {'force': True},
            format='json',
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('confirmation_code', response.json().get('error', ''))
