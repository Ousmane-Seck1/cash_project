from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0020_performance_indexes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferentialSnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation', models.CharField(choices=[('COPY', 'Duplication configuration'), ('LEVEL_COPY', 'Copie referentiel niveau'), ('ROLLBACK', 'Rollback referentiel')], max_length=20)),
                ('payload', models.JSONField(default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('actor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('hopital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referential_snapshots', to='analytics.hopital')),
                ('source_hopital', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='referential_snapshot_sources', to='analytics.hopital')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='referentialsnapshot',
            index=models.Index(fields=['hopital', 'created_at'], name='idx_refsnapshot_hop_date'),
        ),
        migrations.AddIndex(
            model_name='referentialsnapshot',
            index=models.Index(fields=['operation'], name='idx_refsnapshot_op'),
        ),
    ]
