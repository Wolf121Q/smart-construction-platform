from django.contrib.auth.models import Group
from django.db import models
from django.db.models.manager import EmptyManager
from core.models import SuperUser,UserType,User

class Role(Group):
    class Meta:
        proxy=True
        verbose_name = 'Users Roles & Permissions'
        verbose_name_plural = 'Users Roles & Permissions'

    def __str__(self):
        return self.name

class RoleExtra(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On")
    updated_on = models.DateTimeField(auto_now=True, verbose_name="Updated On")
    created_by = models.ForeignKey(SuperUser, null=True, blank=True, verbose_name="Created By",  on_delete=models.CASCADE,related_name="c_%(app_label)s_%(class)s_related",related_query_name="c_%(app_label)s_%(class)ss")
    updated_by = models.ForeignKey(SuperUser, null=True, blank=True, verbose_name="Updated By", on_delete=models.CASCADE,related_name="u_%(app_label)s_%(class)s_related",related_query_name="u_%(app_label)s_%(class)ss")
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Address")
    role = models.OneToOneField(Role,on_delete=models.CASCADE,primary_key=True,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    type = models.ForeignKey(UserType, null=False, blank=False, verbose_name="Role Type", on_delete=models.CASCADE,related_name="c_%(app_label)s_%(class)s_related",related_query_name="c_%(app_label)s_%(class)ss")
    system_code = models.CharField(max_length=100, null=True, blank=True)
    society_id = models.CharField(max_length=100,null=True,blank=True,editable=False)
    description = models.TextField(null=True,blank=True)

    class Meta:
        verbose_name = 'Role Extra Info'
        verbose_name_plural = 'Role Extra Info'
        db_table = 'core_role_extra'

    def __str__(self):
        return self.description

class UserGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    #id = models.BigAutoField(pri)
    user = models.ForeignKey(User,on_delete=EmptyManager,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    group = models.ForeignKey(Role,on_delete=EmptyManager,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    class Meta:
       managed = False
       db_table = 'core_user_groups'