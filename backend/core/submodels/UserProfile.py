from django.contrib.auth.models import User
from core.models import User,SystemStatus
from project.models import Region,City
from django.db import models
import uuid


class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On")
    updated_on = models.DateTimeField(auto_now=True, verbose_name="Updated On")
    created_by = models.ForeignKey(User, null=True,blank=True, verbose_name="Created By", on_delete=models.CASCADE,related_name="c_%(app_label)s_%(class)s_related",related_query_name="c_%(app_label)s_%(class)ss")
    updated_by = models.ForeignKey(User, null=True,blank=True, verbose_name="Updated By", on_delete=models.CASCADE,related_name="u_%(app_label)s_%(class)s_related",related_query_name="u_%(app_label)s_%(class)ss")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    region = models.ForeignKey(Region,null=True,blank=True,editable=True, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    city = models.ForeignKey(City,null=True,blank=True,editable=True, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    status = models.ForeignKey(SystemStatus,editable=True, null=True,blank=True, verbose_name="Flag", on_delete=models.CASCADE,related_name="status_%(app_label)s_%(class)s_related",related_query_name="status_%(app_label)s_%(class)ss")

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        db_table = 'core_user_profiles'