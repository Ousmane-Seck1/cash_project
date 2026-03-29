from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0019_unique_reference_hopital_par_niveau'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='exercice',
            index=models.Index(fields=['hopital', 'annee'], name='idx_exercice_hop_annee'),
        ),
        migrations.AddIndex(
            model_name='exercice',
            index=models.Index(fields=['hopital', 'est_actif', 'est_clos'], name='idx_exercice_hop_statut'),
        ),
        migrations.AddIndex(
            model_name='charge',
            index=models.Index(fields=['exercice', 'date'], name='idx_charge_ex_date'),
        ),
        migrations.AddIndex(
            model_name='charge',
            index=models.Index(fields=['centre_cout'], name='idx_charge_centre'),
        ),
        migrations.AddIndex(
            model_name='charge',
            index=models.Index(fields=['compte'], name='idx_charge_compte'),
        ),
        migrations.AddIndex(
            model_name='produit',
            index=models.Index(fields=['exercice', 'periode'], name='idx_produit_ex_periode'),
        ),
        migrations.AddIndex(
            model_name='produit',
            index=models.Index(fields=['centre_cout'], name='idx_produit_centre'),
        ),
        migrations.AddIndex(
            model_name='resultatcalcul',
            index=models.Index(fields=['exercice', 'centre_cout'], name='idx_resultat_ex_centre'),
        ),
        migrations.AddIndex(
            model_name='resultatcalcul',
            index=models.Index(fields=['resultat_analytique'], name='idx_resultat_value'),
        ),
    ]
