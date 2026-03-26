from django.contrib.auth.models import BaseUserManager
from core.models import SystemType

class UserTypeManager(BaseUserManager):
    def get_queryset(self):
        return super(UserTypeManager, self).get_queryset().filter(parent__system_code="system_type_core_user_type_organization_chart").first().get_descendants()

class UserType(SystemType):
    objects = UserTypeManager()
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.parent = SystemType.objects.get(system_code="system_type_core_user_type_organization_chart")
        return super(UserType, self).save(*args, **kwargs)

    class Admin:
        manager = UserTypeManager()