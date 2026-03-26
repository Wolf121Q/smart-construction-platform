from django.contrib.auth.models import BaseUserManager
from core.models import SystemType

class OranizationHierarcyManager(BaseUserManager):
    def get_queryset(self):
        return super(OranizationHierarcyManager, self).get_queryset()

class OrganizationHierarchy(SystemType):
    objects = OranizationHierarcyManager()
    class Admin:
        manager = OranizationHierarcyManager()
    class Meta:
        proxy = True
        verbose_name = 'Organization Hierarchy'
        verbose_name_plural = 'Organization Hierarchy'
    
    def save(self, *args, **kwargs):
        if self.system_code is None: 
            self.system_code = self.code
        return super(OrganizationHierarchy, self).save(*args, **kwargs)

    # def __str__(self):
    #     return str(self.property_code)