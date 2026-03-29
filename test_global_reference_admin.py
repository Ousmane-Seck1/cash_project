from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.test import TestCase
from rest_framework.test import APIClient

from analytics.models import CentreCout, CentreResponsabilite, CompteCharge, Fonction, Hopital
from analytics.signals import provision_hospital_on_create


class GlobalReferenceAdminTests(TestCase):
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
        self.superuser = User.objects.create_superuser("root", "root@example.com", "rootpass123")
        self.user = User.objects.create_user("user1", "user1@example.com", "pass12345")

        self.hopital_a = Hopital.objects.create(nom="Hopital A", code="HA")
        self.hopital_b = Hopital.objects.create(nom="Hopital B", code="HB")

        self.fonction_a = Fonction.objects.create(hopital=self.hopital_a, code="94.1", libelle="Admin")
        self.fonction_b = Fonction.objects.create(hopital=self.hopital_b, code="94.1", libelle="Admin")

        self.resp_a = CentreResponsabilite.objects.create(
            fonction=self.fonction_a,
            code="94.1.1",
            libelle="Direction",
        )
        self.resp_b = CentreResponsabilite.objects.create(
            fonction=self.fonction_b,
            code="94.1.1",
            libelle="Direction",
        )

        self.centre_a = CentreCout.objects.create(
            centre_responsabilite=self.resp_a,
            code="CC100",
            libelle="Centre 100",
            type_centre="CT_CL",
            unite_oeuvre="acte",
            tarif=100,
            est_actif=True,
        )
        self.centre_b = CentreCout.objects.create(
            centre_responsabilite=self.resp_b,
            code="CC100",
            libelle="Centre 100",
            type_centre="CT_CL",
            unite_oeuvre="acte",
            tarif=100,
            est_actif=True,
        )

        CompteCharge.objects.create(hopital=self.hopital_a, numero="601100", libelle="Achats")
        CompteCharge.objects.create(hopital=self.hopital_b, numero="601100", libelle="Achats")

    def test_non_admin_cannot_modify_reference_data(self):
        self.client.force_login(self.user)

        payload_fonction = {
            "hopital": self.hopital_a.id,
            "code": "94.2",
            "libelle": "Medico-technique",
        }
        resp = self.client.post("/api/fonctions/", payload_fonction, format="json")
        self.assertEqual(resp.status_code, 403)

        payload_compte = {"numero": "602200", "libelle": "Services"}
        resp = self.client.post("/api/comptes-charges/", payload_compte, format="json")
        self.assertEqual(resp.status_code, 403)

    def test_authenticated_user_can_read_reference_data(self):
        self.client.force_login(self.user)

        for url in [
            "/api/fonctions/",
            "/api/centres-responsabilite/",
            "/api/centres-couts/",
            "/api/comptes-charges/",
        ]:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200)

    def test_superuser_create_fonction_propagates_to_all_hospitals(self):
        self.client.force_login(self.superuser)
        payload = {
            "hopital": self.hopital_a.id,
            "code": "94.9",
            "libelle": "Support",
        }
        resp = self.client.post("/api/fonctions/", payload, format="json")
        self.assertEqual(resp.status_code, 201)

        self.assertTrue(Fonction.objects.filter(hopital=self.hopital_a, code="94.9").exists())
        self.assertTrue(Fonction.objects.filter(hopital=self.hopital_b, code="94.9").exists())

    def test_superuser_update_centre_cout_updates_all_hospitals(self):
        self.client.force_login(self.superuser)

        self.centre_b.type_centre = "NT_UO"
        self.centre_b.unite_oeuvre = "journee"
        self.centre_b.tarif = None
        self.centre_b.save(update_fields=["type_centre", "unite_oeuvre", "tarif"])

        url = f"/api/centres-couts/{self.centre_a.id}/"
        payload = {
            "centre_responsabilite": self.resp_a.id,
            "code": "CC100",
            "libelle": "Centre 100 modifie",
            "type_centre": "CT_MT",
            "unite_oeuvre": "examen",
            "tarif": "250.00",
            "ordre_cascade": None,
            "est_actif": True,
        }
        resp = self.client.put(url, payload, format="json")
        self.assertEqual(resp.status_code, 200)

        self.centre_a.refresh_from_db()
        self.centre_b.refresh_from_db()
        self.assertEqual(self.centre_a.libelle, "Centre 100 modifie")
        self.assertEqual(self.centre_b.libelle, "Centre 100 modifie")
        self.assertEqual(self.centre_a.type_centre, "CT_MT")
        self.assertEqual(str(self.centre_a.tarif), "250.00")
        self.assertEqual(self.centre_b.type_centre, "NT_UO")
        self.assertEqual(self.centre_b.unite_oeuvre, "journee")
        self.assertIsNone(self.centre_b.tarif)

    def test_superuser_delete_compte_charge_deletes_all_hospitals(self):
        self.client.force_login(self.superuser)
        compte = CompteCharge.objects.get(hopital=self.hopital_a, numero="601100")
        resp = self.client.delete(f"/api/comptes-charges/{compte.id}/")
        self.assertEqual(resp.status_code, 204)

        self.assertFalse(CompteCharge.objects.filter(numero="601100").exists())
