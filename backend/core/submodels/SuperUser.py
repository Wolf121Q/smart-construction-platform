from django.contrib.auth.models import BaseUserManager
from core.models import User,UserType

class SuperUserManager(BaseUserManager):
    def get_queryset(self):
        return super(SuperUserManager, self).get_queryset().filter(type__system_code="system_type_user_developer_admin")

class SuperUser(User):
    objects = SuperUserManager()
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.type = UserType.objects.get(system_code="system_type_user_developer_admin")
        return super(SuperUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.first_name +" "+self.last_name