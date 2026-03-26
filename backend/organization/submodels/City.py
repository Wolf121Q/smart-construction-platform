from core.models import User,Group
from django.db import models
from django.db.models.manager import EmptyManager
from mptt.models import MPTTModel, TreeForeignKey
from organization.models import Region

class City(MPTTModel):
    id = models.BigAutoField(primary_key=True)
    serial_number = models.CharField(max_length=100, null=True, blank=True, editable=False)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On")
    updated_on = models.DateTimeField(auto_now=True, verbose_name="Updated On")
    created_by = models.ForeignKey(User, null=True, blank=True, verbose_name="Created By", on_delete=models.CASCADE,
                                   related_name="c_%(app_label)s_%(class)s_related",
                                   related_query_name="c_%(app_label)s_%(class)ss",editable=False)
    updated_by = models.ForeignKey(User, null=True, blank=True, verbose_name="Updated By", on_delete=models.CASCADE,
                                   related_name="u_%(app_label)s_%(class)s_related",
                                   related_query_name="u_%(app_label)s_%(class)ss",editable=False)
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Address")

    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=False,blank=False,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    users = models.ManyToManyField(User,blank=True,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    groups = models.ManyToManyField(Group,blank=True,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")


    name = models.CharField(max_length=100,unique=False,null=True,blank=True)
    short_name = models.CharField(max_length=100,unique=False,null=True,blank=True)
    code = models.CharField(max_length=100,null=True,blank=True)

    country_code = models.CharField(max_length=100,unique=False,null=True,blank=True)
    state_code = models.CharField(max_length=100,unique=False,null=True,blank=True)

    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)

    is_division = models.BooleanField(default=False,null=False,blank=False)
    is_district = models.BooleanField(default=False,null=False,blank=False)
    is_tehsil = models.BooleanField(default=False,null=False,blank=False)

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,on_delete=EmptyManager)
    lft = models.IntegerField(default=0,blank=True,null=True,editable=False)
    rght = models.IntegerField(default=0,blank=True,null=True,editable=False)
    tree_id = models.IntegerField(default=0,blank=True,null=True,editable=False)
    mptt_level = models.IntegerField(default=0,blank=True,null=True,editable=False)

    C_STATUS = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )
    status = models.CharField(max_length=20, choices=C_STATUS)

    class MPTTMeta:
        order_insertion_by = ['mptt_level']
        level_attr = 'mptt_level'
    class Meta:
        ordering = ['mptt_level']
        unique_together = ['name', 'code']
        verbose_name = 'city'
        verbose_name_plural = 'cities'
        db_table = 'og_cities'

    def __str__(self):
        return str(self.name)