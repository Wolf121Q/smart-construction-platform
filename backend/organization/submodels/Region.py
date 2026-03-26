from django.db import models
import uuid
from core.models import User,Group

class Region(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    serial_number = models.CharField(max_length=100, null=True, blank=True, editable=False)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On",editable=False)
    updated_on = models.DateTimeField(auto_now=True, verbose_name="Updated On",editable=False)
    created_by = models.ForeignKey(User, null=True, blank=True, verbose_name="Created By", on_delete=models.CASCADE,
                                   related_name="c_%(app_label)s_%(class)s_related",
                                   related_query_name="c_%(app_label)s_%(class)ss",editable=False)
    updated_by = models.ForeignKey(User, null=True, blank=True, verbose_name="Updated By", on_delete=models.CASCADE,
                                   related_name="u_%(app_label)s_%(class)s_related",
                                   related_query_name="u_%(app_label)s_%(class)ss",editable=False)
    users = models.ManyToManyField(User,blank=True,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    groups = models.ManyToManyField(Group,blank=True,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Address",editable=False)
    name = models.CharField(max_length=100,unique=True)
    ordering = models.CharField(max_length=100,null=True,blank=True,verbose_name="Ordering")
    code = models.CharField(max_length=100,unique=True,null=True,blank=True)

    C_STATUS = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )
    status = models.CharField(max_length=20, choices=C_STATUS)

    def __str__(self):
        # return "name" from translation
        return str(self.name)
    def __unicode__(self):
        return str(self.name)
    class Meta:
        unique_together = ['name','code']
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'
        db_table = 'og_region'