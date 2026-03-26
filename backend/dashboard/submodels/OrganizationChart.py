from django.contrib.auth.models import BaseUserManager
from project.models import Project

class OrganizationChartManager(BaseUserManager):
    def get_queryset(self):
        return super(OrganizationChartManager, self).get_queryset()

class OrganizationChart(Project):
    objects = OrganizationChartManager()
    class Admin:
        manager = OrganizationChartManager()
    class Meta:
        proxy = True
        verbose_name = 'Organizational Hierarchy'
        verbose_name_plural = 'Organizational Hierarchy'
    def save(self, *args, **kwargs):
        #self.status_type = MemberStatusType.objects.get(system_code="member_owner")
        return super(OrganizationChart, self).save(*args, **kwargs)

    # def __str__(self):
    #     return str(self.property_code)