from django.db import models

class AppVersionManager(models.Manager):
    def get_queryset(self):
        return super(AppVersionManager, self).get_queryset().filter()

class AppVersion(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On")
    updated_on = models.DateTimeField(null=True, blank=True, verbose_name="Updated On")
    created_by = models.ForeignKey('self', null=True, blank=True, verbose_name="Created By",  on_delete=models.CASCADE,related_name="c_%(app_label)s_%(class)s_related",related_query_name="c_%(app_label)s_%(class)ss")
    updated_by = models.ForeignKey('self', null=True, blank=True, verbose_name="Updated By", on_delete=models.CASCADE,related_name="u_%(app_label)s_%(class)s_related",related_query_name="u_%(app_label)s_%(class)ss")
    name = models.CharField(max_length=100, unique=False)
    APP_TYPE = (
        ("android", "Android"),
        ("ios", "IOS"),
    )
    type = models.CharField(default='android',max_length=20, choices=APP_TYPE, blank=False, null=False)
    version = models.PositiveSmallIntegerField(verbose_name='Version')
   
    objects = AppVersionManager()
 
    class Meta:
        unique_together = ('type','version')
        verbose_name = 'App Version'
        verbose_name_plural = 'App Versions'
        db_table = 'pro_app_version'

    def __str__(self):
        ctx = {
            'name': self.name,
            'type': self.type,
            'version': self.version,
        }
        return u'%(name)s - %(type)s - %(version)s' % ctx
       