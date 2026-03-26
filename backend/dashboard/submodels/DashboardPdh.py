from django.contrib.auth.models import BaseUserManager
from project.models import Project

class DashboardManager(BaseUserManager):
    def get_queryset(self):
        return super(DashboardManager, self).get_queryset()

class DashboardPdh(Project):
    objects = DashboardManager()
    class Admin:
        manager = DashboardManager()
    class Meta:
        proxy = True
        verbose_name = 'Login History'
        verbose_name_plural = 'Login History'
    def save(self, *args, **kwargs):
        #self.status_type = MemberStatusType.objects.get(system_code="member_owner")
        return super(DashboardPdh, self).save(*args, **kwargs)

    # def __str__(self):
    #     return str(self.property_code)