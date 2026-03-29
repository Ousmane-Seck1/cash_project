from datetime import date

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.test import TestCase
from rest_framework.test import APIClient

from analytics.models import (
    CentreCout,
    CentreResponsabilite,
    Charge,
    CompteCharge,
    Exercice,
    Fonction,
    Hopital,
    Produit,
    ResultatCalcul,
)
from analytics.signals import provision_hospital_on_create


class SuperuserQualityAndLevelTests(TestCase):
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

        self.h1 = Hopital.objects.create(nom='Hopital N1', code='HN1', niveau='N1')
        self.h2 = Hopital.objects.create(nom='Hopital N2', code='HN2', niveau='N2')

        ex1 = Exercice.objects.create(
            hopital=self.h1,
            annee=2025,
            date_debut=date(2025, 1, 1),
            date_fin=date(2025, 12, 31),
            est_actif=True,
            est_clos=False,
        )
        ex2 = Exercice.objects.create(
            hopital=self.h2,
            annee=2025,
            date_debut=date(2025, 1, 1),
            date_fin=date(2025, 12, 31),
            est_actif=True,
            est_clos=False,
        )

        f1 = Fonction.objects.create(hopital=self.h1, code='94.1', libelle='Admin')
        r1 = CentreResponsabilite.objects.create(fonction=f1, code='94.1.1', libelle='Direction')
        c1 = CentreCout.objects.create(
            centre_responsabilite=r1,
            code='C1',
            libelle='Centre 1',
            type_centre='CT_CL',
            unite_oeuvre='acte',
            tarif=100,
            est_actif=True,
        )
        cp1 = CompteCharge.objects.create(hopital=self.h1, numero='601100', libelle='Achats')

        f2 = Fonction.objects.create(hopital=self.h2, code='94.1', libelle='Admin')
        r2 = CentreResponsabilite.objects.create(fonction=f2, code='94.1.1', libelle='Direction')
        c2 = CentreCout.objects.create(
            centre_responsabilite=r2,
            code='C1',
            libelle='Centre 1',
            type_centre='CT_CL',
            unite_oeuvre='acte',
            tarif=100,
            est_actif=True,
        )
        cp2 = CompteCharge.objects.create(hopital=self.h2, numero='601100', libelle='Achats')

        Charge.objects.create(exercice=ex1, date=date(2025, 1, 1), designation='c1', montant=100, centre_cout=c1, compte=cp1)
        Produit.objects.create(exercice=ex1, centre_cout=c1, periode=1, type_produit='ORDINAIRE', montant=200)
        ResultatCalcul.objects.create(exercice=ex1, centre_cout=c1, charges_totales=100, resultat_analytique=100)

        Charge.objects.create(exercice=ex2, date=date(2025, 1, 1), designation='c2', montant=80, centre_cout=c2, compte=cp2)
        Produit.objects.create(exercice=ex2, centre_cout=c2, periode=1, type_produit='ORDINAIRE', montant=90)
        ResultatCalcul.objects.create(exercice=ex2, centre_cout=c2, charges_totales=80, resultat_analytique=10)

    def test_comparaison_interhopitaux_filter_by_level(self):
        self.client.force_login(self.superuser)
        response = self.client.get('/api/hopitaux/comparaison_interhopitaux/?niveaux=N2&annee=2025')
        self.assertEqual(response.status_code, 200)
        payload = response.json()

        self.assertEqual(len(payload['rows']), 1)
        self.assertEqual(payload['rows'][0]['hopital_code'], 'HN2')
        self.assertIn('kpis_par_niveau', payload)
        self.assertIn('N2', payload['kpis_par_niveau'])

    def test_controle_qualite_donnees_exposes_anomalies(self):
        self.client.force_login(self.superuser)
        response = self.client.get('/api/hopitaux/controle_qualite_donnees/')
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn('summary', payload)
        self.assertIn('anomalies', payload)
