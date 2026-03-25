from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

from .hospital_databases import ensure_hospital_database
from .models import Exercice, Hopital


@receiver(post_save, sender=Hopital)
def provision_hospital_on_create(sender, instance, created, **kwargs):
    """Garantit la base dédiée et un exercice courant lors de la création d'un hôpital."""
    if not created:
        return

    current_year = datetime.now().year
    Exercice.objects.get_or_create(
        hopital=instance,
        annee=current_year,
        defaults={
            'date_debut': f'{current_year}-01-01',
            'date_fin': f'{current_year}-12-31',
            'est_actif': True,
            'est_clos': False,
        },
    )

    ensure_hospital_database(instance)
