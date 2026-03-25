from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0016_hopitalrole_userprofile_hopital_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='hopital',
            name='database_alias',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='hopital',
            name='database_name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
