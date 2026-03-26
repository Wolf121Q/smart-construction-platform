from django.contrib.auth.models import BaseUserManager
from project.models import Project

class PdhManager(BaseUserManager):
    def get_queryset(self):
        return super(PdhManager, self).get_queryset()
class Pdh(Project):
    objects = PdhManager()
    class Admin:
        manager = PdhManager()
    class Meta:
        proxy = True
        verbose_name = 'PDH Summary'
        verbose_name_plural = 'PDH Summary'
    def save(self, *args, **kwargs):
        #self.status_type = MemberStatusType.objects.get(system_code="member_owner")
        return super(Pdh, self).save(*args, **kwargs)

    # def __str__(self):
    #     return str(self.property_code)