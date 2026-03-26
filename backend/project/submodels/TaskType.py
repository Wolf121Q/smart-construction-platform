from core.models import BaseUserManager
from core.models import SystemStatus

class TaskTypeManager(BaseUserManager):
    def get_queryset(self):
        return super(TaskTypeManager, self).get_queryset().filter(parent__system_code = 'system_status_task_status_material')

class TaskType(SystemStatus):
    objects = TaskTypeManager()
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.parent = SystemStatus.objects.get(system_code = "system_status_task_status")
        return super(TaskType, self).save(*args, **kwargs)

    class Admin:
        manager = TaskTypeManager()