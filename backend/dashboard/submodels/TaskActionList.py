from django.contrib.auth.models import BaseUserManager
from project.models import TaskAction

class TaskActionManager(BaseUserManager):
    def get_queryset(self):
        return super(TaskActionManager, self).get_queryset()

class TaskActionList(TaskAction):
    objects = TaskActionManager()
    class Admin:
        manager = TaskActionManager()
    class Meta:
        proxy = True
        verbose_name = 'Flags'
        verbose_name_plural = 'Flags'
        permissions = [
            ('can_delete_flag', 'Can delete flag'),
        ]

    def save(self, *args, **kwargs):
        #self.status_type = MemberStatusType.objects.get(system_code="member_owner")
        return super(TaskActionList, self).save(*args, **kwargs)
    

    
    # def __str__(self):
    #     return str(self.property_code)