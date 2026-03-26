from django.core.management.base import BaseCommand
from project.models import TaskAction,TaskActionComment,TaskFile,TaskActionTimeLine

class Command(BaseCommand):
    help = 'Your custom command help text'

    def handle(self, *args, **options):
        # Your command logic goes here
        task_action_qs = TaskAction.objects.filter(status__system_code__in = ['system_status_task_status_material_green','system_status_task_status_inspection_green'])
        for task_action in task_action_qs:
            task_action_comment = TaskActionComment.objects.filter(task_action_id = task_action.id,reply=False).first()
            if task_action_comment:
                self.stdout.write(self.style.WARNING('Before:'))
                self.stdout.write(self.style.WARNING(task_action.description))
                task_action.description = task_action_comment.description
                task_action.save()
                self.stdout.write(self.style.SUCCESS('After:'))
                self.stdout.write(self.style.SUCCESS(task_action.description))