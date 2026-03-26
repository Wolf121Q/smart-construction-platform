from core.models import BaseUserManager
from core.models import SystemStatus

class TaskStatusManager(BaseUserManager):
    def get_queryset(self):
        return super(TaskStatusManager, self).get_queryset().filter(parent__system_code__in =['system_status_task_status_material','system_status_task_status_inspection'])

class TaskStatus(SystemStatus):
    objects = TaskStatusManager()
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        #self.parent = SystemStatus.objects.get(system_code = "system_status_complaints")
        return super(TaskStatus, self).save(*args, **kwargs)

    class Admin:
        manager = TaskStatusManager()