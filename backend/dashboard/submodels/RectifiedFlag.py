from django.contrib.auth.models import BaseUserManager
from project.models import TaskAction

class RectifiedFlagManager(BaseUserManager):
    def get_queryset(self):
        return super(RectifiedFlagManager, self).get_queryset()

class RectifiedFlag(TaskAction):
    objects = RectifiedFlagManager()
    class Admin:
        manager = RectifiedFlagManager()
    class Meta:
        proxy = True
        verbose_name = 'Rectified Flags'
        verbose_name_plural = 'Rectified Flags'
    def save(self, *args, **kwargs):
        #self.status_type = MemberStatusType.objects.get(system_code="member_owner")
        return super(RectifiedFlag, self).save(*args, **kwargs)

    # def __str__(self):
    #     return str(self.property_code)