from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from analytics.models import UserProfile

class Command(BaseCommand):
    help = 'Create user profiles for existing users'

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': 'controleur'}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created profile for {user.username} with role controleur')
                )
            else:
                self.stdout.write(
                    f'Profile already exists for {user.username} (role: {profile.role})'
                )