from django.contrib.auth.models import BaseUserManager
from project.models import Project
from django.db.models import Q

class ReportManager(BaseUserManager):
    def get_queryset(self):
        return super(ReportManager, self).get_queryset()

class Report(Project):
    objects = ReportManager()
    class Admin:
        manager = ReportManager()
    class Meta:
        proxy = True
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
    def save(self, *args, **kwargs):
        #self.status_type = MemberStatusType.objects.get(system_code="member_owner")
        return super(Report, self).save(*args, **kwargs)

    # def __str__(self):
    #     return str(self.property_code)