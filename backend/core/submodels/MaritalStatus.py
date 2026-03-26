from django.contrib.auth.models import BaseUserManager
from core.models import SystemStatus

class MaritalStatusManager(BaseUserManager):
    def get_queryset(self):
        return super(MaritalStatusManager, self).get_queryset().filter(parent__system_code="system_status_core_marital_status")

class MaritalStatus(SystemStatus):
    objects = MaritalStatusManager()
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.parent = SystemStatus.objects.get(system_code="system_status_core_marital_status")
        return super(MaritalStatus, self).save(*args, **kwargs)

    class Admin:
        manager = MaritalStatusManager()