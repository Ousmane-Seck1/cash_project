from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0017_hopital_database_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='hopital',
            name='est_reference_niveau',
            field=models.BooleanField(
                default=False,
                help_text='Indique si cet hopital est la reference a copier pour son niveau.',
            ),
        ),
        migrations.AddField(
            model_name='hopital',
            name='niveau',
            field=models.CharField(
                choices=[('N1', 'Niveau 1'), ('N2', 'Niveau 2'), ('N3', 'Niveau 3')],
                default='N1',
                max_length=2,
            ),
        ),
    ]
