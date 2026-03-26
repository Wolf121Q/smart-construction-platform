from django.contrib.auth.models import BaseUserManager
from project.models import TaskAction

class ProjectDirectorHousingManager(BaseUserManager):
    def get_queryset(self):
        return super(ProjectDirectorHousingManager, self).get_queryset()

class ProjectDirectorHousing(TaskAction):
    objects = ProjectDirectorHousingManager()
    class Admin:
        manager = ProjectDirectorHousingManager()
    class Meta:
        proxy = True
        verbose_name = 'Dashboard'
        verbose_name_plural = 'Dashboard'

    def save(self, *args, **kwargs):
        #self.status_type = MemberStatusType.objects.get(system_code="member_owner")
        return super(ProjectDirectorHousing, self).save(*args, **kwargs)

    # def __str__(self):
    #     return str(self.property_code)