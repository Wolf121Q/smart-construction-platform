from django.contrib.auth.models import BaseUserManager
from project.models import Project

class CADetailManager(BaseUserManager):
    def get_queryset(self):
        return super(CADetailManager, self).get_queryset()

class CADetail(Project):
    objects = CADetailManager()
    class Admin:
        manager = CADetailManager()
    class Meta:
        proxy = True
        verbose_name = 'Project Details'
        verbose_name_plural = 'Project Details'

    def save(self, *args, **kwargs):
        #self.status_type = MemberStatusType.objects.get(system_code="member_owner")
        return super(CADetail, self).save(*args, **kwargs)

    # def __str__(self):
    #     return str(self.property_code)