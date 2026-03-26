from django.core.management.base import BaseCommand
from core.models import UserProfile,User  # Import your UserProfile model
from project.models import Project

class Command(BaseCommand):
    help = 'Create user profiles for users without profiles'

    def handle(self, *args, **options):
        # # Get a list of users who don't have profiles
        users_without_profiles = User.objects.filter(c_core_userprofiles__isnull=True)
        # Create profiles for these users
        for user in users_without_profiles:
            if not UserProfile.objects.filter(user=user).exists():
                UserProfile.objects.create(user=user)
                self.stdout.write(self.style.SUCCESS(f'Created profile for user: {user.username}'))
            else:
                self.stdout.write(self.style.WARNING(f'Profile already exists for user: {user.username}'))