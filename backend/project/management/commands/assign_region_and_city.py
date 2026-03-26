from django.core.management.base import BaseCommand
from core.models import UserProfile

class Command(BaseCommand):
    help = 'Assigns the region and city of the first project to user profiles.'

    def handle(self, *args, **options):
        self.assign_region_and_city()

    def assign_region_and_city(self):
        user_profiles = UserProfile.objects.all()

        for user_profile in user_profiles:
            # if user_profile.regions is None and user_profile.cities is None:
            user_profile_projects = user_profile.projects.all()

            # Get unique cities and regions from all projects
            unique_cities = set()
            unique_regions = set()
            
            if user_profile_projects.exists():
                for project in user_profile_projects:
                    unique_cities.add(project.city)
                    unique_regions.add(project.region)
                user_profile.regions.set(unique_regions)
                user_profile.cities.set(unique_cities)
                user_profile.save()
                self.stdout.write(self.style.SUCCESS(f'Region and city assigned successfully to user {user_profile.user}'))

