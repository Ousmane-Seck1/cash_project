from django.db import migrations, models


def deduplicate_level_references(apps, schema_editor):
    Hopital = apps.get_model('analytics', 'Hopital')

    for niveau, _ in [('N1', 'Niveau 1'), ('N2', 'Niveau 2'), ('N3', 'Niveau 3')]:
        refs = list(Hopital.objects.filter(niveau=niveau, est_reference_niveau=True).order_by('id'))
        if len(refs) <= 1:
            continue

        for hopital in refs[1:]:
            hopital.est_reference_niveau = False
            hopital.save(update_fields=['est_reference_niveau'])


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0018_hopital_niveau_reference'),
    ]

    operations = [
        migrations.RunPython(deduplicate_level_references, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name='hopital',
            constraint=models.UniqueConstraint(
                condition=models.Q(est_reference_niveau=True),
                fields=('niveau',),
                name='unique_reference_hopital_par_niveau',
            ),
        ),
    ]
