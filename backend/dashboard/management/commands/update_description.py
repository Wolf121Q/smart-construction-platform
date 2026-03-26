from django.core.management.base import BaseCommand
from datetime import datetime
from project.models import TaskAction

class Command(BaseCommand):
    help = 'Update descriptions (if "rectified" is not present)'

    def handle(self, *args, **kwargs):
        qs = TaskAction.objects.filter(parent__isnull=False,status__system_code__in = ['system_status_task_status_material_green','system_status_task_status_inspection_green'])
        for obj in qs:
            if "rectified" not in obj.description.lower():
                obj.description += " (Rectified)"
                obj.save()
            self.stdout.write(self.style.SUCCESS(f'Updated description for object {obj.pk}'))


