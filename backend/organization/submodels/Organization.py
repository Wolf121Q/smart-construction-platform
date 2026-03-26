from django.db import models
from core.models import User,Group
import uuid
from organization.models import City,Region,Type
from django.db.models.manager import EmptyManager


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    serial_number = models.CharField(max_length=100, null=True, blank=True, editable=False)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On",editable=False)
    updated_on = models.DateTimeField(auto_now=True, verbose_name="Updated On",editable=False)
    created_by = models.ForeignKey(User, null=True, blank=True,  verbose_name="Created By",  on_delete=EmptyManager,related_name="c_%(app_label)s_%(class)s_related",related_query_name="c_%(app_label)s_%(class)ss",editable=False)
    updated_by = models.ForeignKey(User, null=True, blank=True,  verbose_name="Updated By", on_delete=EmptyManager,related_name="u_%(app_label)s_%(class)s_related",related_query_name="u_%(app_label)s_%(class)ss",editable=False)
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Address",editable=False)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100,unique=True)
    phone = models.CharField(max_length=100,unique=True)
    fax = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    description = models.TextField(null=True,blank=True)

    users = models.ManyToManyField(User,blank=True,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    groups = models.ManyToManyField(Group,blank=True,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")

    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")

    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100,null=True,blank=True)
    zipcode = models.CharField(max_length=10)


    C_STATUS = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )
    status = models.CharField(max_length=20, choices=C_STATUS)


    class Meta:
        unique_together = (('region','city','type', 'code',))
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
        db_table = 'og_organizations'

    def __str__(self):
        return str(self.name)
