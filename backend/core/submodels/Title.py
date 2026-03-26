from django.contrib.auth.models import BaseUserManager
from core.models import SystemType

class TitleManager(BaseUserManager):
    def get_queryset(self):
        return super(TitleManager, self).get_queryset().filter(parent__system_code="system_type_core_title")

class Title(SystemType):
    objects = TitleManager()
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.parent = SystemType.objects.get(system_code="system_type_core_title")
        return super(Title, self).save(*args, **kwargs)

    class Admin:
        manager = TitleManager()