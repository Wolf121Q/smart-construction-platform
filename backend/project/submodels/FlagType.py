from django.contrib.auth.models import BaseUserManager
from core.models import SystemType

class FlagTypeManager(BaseUserManager):
    def get_queryset(self):
        return super(FlagTypeManager, self).get_queryset().filter(system_code__in = ["system_type_flag_type_red","system_type_flag_type_yellow","system_type_flag_type_orange","system_type_flag_type_green"])

class FlagType(SystemType):
    objects = FlagTypeManager()
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        return super(FlagType, self).save(*args, **kwargs)

    class Admin:
        manager = FlagTypeManager()