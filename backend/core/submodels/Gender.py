from django.contrib.auth.models import BaseUserManager
from core.models import SystemType

class GenderManager(BaseUserManager):
    def get_queryset(self):
        return super(GenderManager, self).get_queryset().filter(parent__system_code="system_type_core_gender")

class Gender(SystemType):
    objects = GenderManager()
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.parent = SystemType.objects.get(system_code="system_type_core_gender")
        return super(Gender, self).save(*args, **kwargs)

    class Admin:
        manager = GenderManager()