from django.core.management.base import BaseCommand
from core.models import UserProfile

class Command(BaseCommand):
    help = 'Assigns the projects to user in user profiles.'

    def handle(self, *args, **options):
        self.assign_projects_in_user_profile()

    def assign_projects_in_user_profile(self):
        user_profiles = UserProfile.objects.all()

        for user_profile in user_profiles:
            if not user_profile.projects.exists():
                user = user_profile.user
                user_projects = user.project_project_related.all()
                if user_projects.exists():
                    user_profile.projects.set(user_projects)
                    user_profile.save()
                    self.stdout.write(self.style.SUCCESS(f'User Profile of User {user_profile.user} is assigned with all projects'))
