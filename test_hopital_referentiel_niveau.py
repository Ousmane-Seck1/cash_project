from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.test import TestCase
from rest_framework.test import APIClient

from analytics.models import CentreCout, CentreResponsabilite, CompteCharge, Fonction, Hopital
from analytics.signals import provision_hospital_on_create


class HopitalReferentielNiveauTests(TestCase):
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

        self.reference_n2 = Hopital.objects.create(
            nom="Reference Niveau 2",
            code="REFN2",
            niveau="N2",
            est_reference_niveau=True,
        )
        self.target_n2 = Hopital.objects.create(
            nom="Hopital Niveau 2 Cible",
            code="TGTN2",
            niveau="N2",
            est_reference_niveau=False,
        )
        self.other_n1 = Hopital.objects.create(
            nom="Reference Niveau 1",
            code="REFN1",
            niveau="N1",
            est_reference_niveau=True,
        )

        ref_fonction = Fonction.objects.create(hopital=self.reference_n2, code="94.2", libelle="Medico-technique")
        ref_resp = CentreResponsabilite.objects.create(fonction=ref_fonction, code="94.2.8", libelle="Buanderie")
        CentreCout.objects.create(
            centre_responsabilite=ref_resp,
            code="BLD01",
            libelle="Buanderie",
            type_centre="NT_UO",
            unite_oeuvre="kg linge",
            tarif=None,
            est_actif=True,
        )
        CompteCharge.objects.create(hopital=self.reference_n2, numero="606100", libelle="Consommables buanderie")

        tgt_fonction = Fonction.objects.create(hopital=self.target_n2, code="94.2", libelle="Medico-technique")
        tgt_resp = CentreResponsabilite.objects.create(fonction=tgt_fonction, code="94.2.8", libelle="Buanderie")
        self.target_center = CentreCout.objects.create(
            centre_responsabilite=tgt_resp,
            code="BLD01",
            libelle="Buanderie locale",
            type_centre="NT_TF",
            unite_oeuvre="",
            tarif=None,
            est_actif=True,
        )

    def test_copy_reference_by_level_uses_same_level_source(self):
        self.client.force_login(self.superuser)

        response = self.client.post(
            f"/api/hopitaux/{self.target_n2.id}/copier_referentiel_niveau/",
            {},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["niveau"], "N2")
        self.assertEqual(payload["source_hopital"]["id"], self.reference_n2.id)

        self.assertTrue(Fonction.objects.filter(hopital=self.target_n2, code="94.2").exists())
        self.assertTrue(CompteCharge.objects.filter(hopital=self.target_n2, numero="606100").exists())

    def test_copy_reference_by_level_preserves_local_center_parameters_by_default(self):
        self.client.force_login(self.superuser)

        response = self.client.post(
            f"/api/hopitaux/{self.target_n2.id}/copier_referentiel_niveau/",
            {},
            format="json",
        )
        self.assertEqual(response.status_code, 200)

        self.target_center.refresh_from_db()
        self.assertEqual(self.target_center.libelle, "Buanderie")
        self.assertEqual(self.target_center.type_centre, "NT_TF")
        self.assertEqual(self.target_center.unite_oeuvre, "")

    def test_copy_reference_by_level_can_force_center_parameters(self):
        self.client.force_login(self.superuser)

        response = self.client.post(
            f"/api/hopitaux/{self.target_n2.id}/copier_referentiel_niveau/",
            {"force": True, "confirmation_code": "CONFIRMER"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)

        self.target_center.refresh_from_db()
        self.assertEqual(self.target_center.type_centre, "NT_UO")
        self.assertEqual(self.target_center.unite_oeuvre, "kg linge")

    def test_copy_reference_by_level_rejects_source_with_different_level(self):
        self.client.force_login(self.superuser)

        response = self.client.post(
            f"/api/hopitaux/{self.target_n2.id}/copier_referentiel_niveau/",
            {"source_hopital_id": self.other_n1.id},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_copy_reference_by_level_preview_only_returns_diff(self):
        self.client.force_login(self.superuser)

        response = self.client.post(
            f"/api/hopitaux/{self.target_n2.id}/copier_referentiel_niveau/",
            {"preview_only": True},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload.get('preview_only'))
        self.assertIn('diff', payload)
        self.assertIn('centres_cout', payload['diff'])

    def test_unique_reference_per_level_enforced(self):
        self.client.force_login(self.superuser)

        response = self.client.patch(
            f"/api/hopitaux/{self.target_n2.id}/",
            {"est_reference_niveau": True},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_rollback_referentiel_on_selected_section(self):
        self.client.force_login(self.superuser)

        copy_response = self.client.post(
            f"/api/hopitaux/{self.target_n2.id}/copier_referentiel_niveau/",
            {},
            format="json",
        )
        self.assertEqual(copy_response.status_code, 200)
        snapshot_id = copy_response.json().get('snapshot_id')
        self.assertIsNotNone(snapshot_id)

        CompteCharge.objects.create(hopital=self.target_n2, numero="999999", libelle="Temporaire")
        self.assertTrue(CompteCharge.objects.filter(hopital=self.target_n2, numero="999999").exists())

        rollback_response = self.client.post(
            f"/api/hopitaux/{self.target_n2.id}/rollback_referentiel/",
            {
                "snapshot_id": snapshot_id,
                "sections": ["comptes_charges"],
                "confirmation_code": "CONFIRMER",
            },
            format="json",
        )
        self.assertEqual(rollback_response.status_code, 200)
        self.assertFalse(CompteCharge.objects.filter(hopital=self.target_n2, numero="999999").exists())
