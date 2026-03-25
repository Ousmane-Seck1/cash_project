from datetime import date

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.test import TestCase
from rest_framework.test import APIClient

from analytics.models import (
    Charge,
    CompteCharge,
    Exercice,
    Fonction,
    Hopital,
    CentreResponsabilite,
    CentreCout,
    Produit,
    ResultatCalcul,
)
from analytics.signals import provision_hospital_on_create


class InterHopitauxApiTests(TestCase):
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
        self.superuser = User.objects.create_superuser(
            username='root',
            email='root@example.com',
            password='rootpass123',
        )
        self.standard_user = User.objects.create_user(
            username='agent',
            email='agent@example.com',
            password='agentpass123',
        )

        self.hopital_a = Hopital.objects.create(nom='Hopital A', code='HA')
        self.hopital_b = Hopital.objects.create(nom='Hopital B', code='HB')

        self.exercice_a_2025 = Exercice.objects.create(
            hopital=self.hopital_a,
            annee=2025,
            date_debut=date(2025, 1, 1),
            date_fin=date(2025, 12, 31),
            est_actif=True,
            est_clos=False,
        )
        self.exercice_b_2025 = Exercice.objects.create(
            hopital=self.hopital_b,
            annee=2025,
            date_debut=date(2025, 1, 1),
            date_fin=date(2025, 12, 31),
            est_actif=False,
            est_clos=False,
        )

        self._seed_financial_data(
            hopital=self.hopital_a,
            exercice=self.exercice_a_2025,
            fonction_code='94.1',
            resp_code='94.1.1',
            centre_code='94.1.1.1',
            compte_numero='601100',
            charge_montant=1000,
            produit_montant=1400,
            resultat=400,
        )
        self._seed_financial_data(
            hopital=self.hopital_b,
            exercice=self.exercice_b_2025,
            fonction_code='94.2',
            resp_code='94.2.1',
            centre_code='94.2.1.1',
            compte_numero='602200',
            charge_montant=800,
            produit_montant=700,
            resultat=-100,
        )

    def _seed_financial_data(
        self,
        hopital,
        exercice,
        fonction_code,
        resp_code,
        centre_code,
        compte_numero,
        charge_montant,
        produit_montant,
        resultat,
    ):
        fonction = Fonction.objects.create(hopital=hopital, code=fonction_code, libelle=f'Fonction {fonction_code}')
        responsabilite = CentreResponsabilite.objects.create(
            fonction=fonction,
            code=resp_code,
            libelle=f'Resp {resp_code}',
        )
        centre = CentreCout.objects.create(
            centre_responsabilite=responsabilite,
            code=centre_code,
            libelle=f'Centre {centre_code}',
            type_centre='CT_CL',
            unite_oeuvre='acte',
            tarif=100,
        )
        compte = CompteCharge.objects.create(hopital=hopital, numero=compte_numero, libelle='Compte test')

        Charge.objects.create(
            exercice=exercice,
            date=date(exercice.annee, 1, 15),
            designation='Charge test',
            compte=compte,
            montant=charge_montant,
            centre_cout=centre,
        )
        Produit.objects.create(
            exercice=exercice,
            centre_cout=centre,
            periode=1,
            type_produit=Produit.TYPE_ORDINAIRE,
            montant=produit_montant,
        )
        ResultatCalcul.objects.create(
            exercice=exercice,
            centre_cout=centre,
            charges_directes=charge_montant,
            charges_indirectes=0,
            charges_totales=charge_montant,
            produits=produit_montant,
            volume_activite=10,
            cout_revient_unitaire=10,
            resultat_analytique=resultat,
        )

    def test_comparaison_interhopitaux_requires_superuser(self):
        self.client.force_login(self.standard_user)
        response = self.client.get('/api/hopitaux/comparaison_interhopitaux/')
        self.assertEqual(response.status_code, 403)

    def test_comparaison_interhopitaux_returns_expected_payload_for_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.get('/api/hopitaux/comparaison_interhopitaux/?annee=2025')

        self.assertEqual(response.status_code, 200)
        payload = response.json()

        self.assertIn('rows', payload)
        self.assertIn('kpis', payload)
        self.assertIn('top_flop', payload)
        self.assertIn('alertes', payload)
        self.assertEqual(len(payload['rows']), 2)

        rows_by_code = {row['hopital_code']: row for row in payload['rows']}
        self.assertAlmostEqual(rows_by_code['HA']['charges'], 1000.0)
        self.assertAlmostEqual(rows_by_code['HA']['produits'], 1400.0)
        self.assertAlmostEqual(rows_by_code['HA']['resultat'], 400.0)

        self.assertAlmostEqual(rows_by_code['HB']['charges'], 800.0)
        self.assertAlmostEqual(rows_by_code['HB']['produits'], 700.0)
        self.assertAlmostEqual(rows_by_code['HB']['resultat'], -100.0)

    def test_comparaison_interhopitaux_filters_actifs_only(self):
        self.client.force_login(self.superuser)
        response = self.client.get('/api/hopitaux/comparaison_interhopitaux/?actifs_seulement=1')

        self.assertEqual(response.status_code, 200)
        rows = response.json()['rows']
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['hopital_code'], 'HA')
        self.assertTrue(rows[0]['exercice_actif'])

    def test_comparaison_interhopitaux_filters_selected_hospitals(self):
        self.client.force_login(self.superuser)
        url = f'/api/hopitaux/comparaison_interhopitaux/?hopitaux={self.hopital_b.id}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        rows = response.json()['rows']
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['hopital_id'], self.hopital_b.id)

    def test_comparaison_interhopitaux_rejects_invalid_annee(self):
        self.client.force_login(self.superuser)
        response = self.client.get('/api/hopitaux/comparaison_interhopitaux/?annee=abc')

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_exports_interhopitaux_excel_and_pdf(self):
        self.client.force_login(self.superuser)

        excel_response = self.client.get('/api/hopitaux/export_comparaison_interhopitaux/?annee=2025')
        self.assertEqual(excel_response.status_code, 200)
        self.assertIn(
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            excel_response['Content-Type'],
        )

        pdf_response = self.client.get('/api/hopitaux/export_comparaison_interhopitaux_pdf/?annee=2025')
        self.assertEqual(pdf_response.status_code, 200)
        self.assertIn('application/pdf', pdf_response['Content-Type'])
