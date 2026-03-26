from django.db import models
from core.models import User,Group
from core.models import SystemStatus
from organization.models import City,Region,Type,Organization
from project.models import Category
from django.db.models.manager import EmptyManager
from utils.Upload import Upload
from mptt.models import TreeForeignKey
from vendor_company.models import VendorCompany


class QuillProject(models.Model):
    serial_number = models.CharField(max_length=100, null=True, blank=True, editable=False)
    reference_number = models.CharField(max_length=100, null=True, blank=True, editable=False,verbose_name="Ref CA")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On",editable=False)
    updated_on = models.DateTimeField(auto_now=True, verbose_name="Updated On",editable=False)
    created_by = models.ForeignKey(User, null=True, blank=True,  verbose_name="Created By",  on_delete=EmptyManager,related_name="c_%(app_label)s_%(class)s_related",related_query_name="c_%(app_label)s_%(class)ss",editable=False)
    updated_by = models.ForeignKey(User, null=True, blank=True,  verbose_name="Updated By", on_delete=EmptyManager,related_name="u_%(app_label)s_%(class)s_related",related_query_name="u_%(app_label)s_%(class)ss",editable=False)
  
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Address", editable=False)

    users = models.ManyToManyField(User,null=True,blank=True,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    groups = models.ManyToManyField(Group,null=True,blank=True,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")

    name = models.CharField(max_length=100,verbose_name="Name of Project")
    code = models.CharField(max_length=100,unique=True, verbose_name='CA NO')
    description = models.TextField(null=True,blank=True)

    status = TreeForeignKey(SystemStatus,null=False,blank=False, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    category = TreeForeignKey(Category,null=False,blank=False, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    region = models.ForeignKey(Region,null=True,blank=True,editable=False, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    city = models.ForeignKey(City,verbose_name = "Station",null=True,blank=True,editable=False, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    type = models.ForeignKey(Type,null=True,blank=True,editable=False, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    contractor = models.ForeignKey(VendorCompany,null=True,blank=True,verbose_name = "Contractor", on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    organization = models.ForeignKey(Organization,verbose_name = "Site",on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    thumbnail = models.ImageField(null=True,blank=True,upload_to=Upload)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    progress_planned = models.DecimalField(default=0.0,max_digits = 5,decimal_places = 2,blank=True, null=True)
    progress_actual = models.DecimalField(default=0.0,max_digits = 5,decimal_places = 2,blank=True, null=True)
    start_date_actual = models.DateField(blank=True, null=True)
    end_date_actual = models.DateField(blank=True, null=True)
    time_lapsed_percentage = models.FloatField(blank=True, null=True)
    time_lapsed_date = models.DateField(blank=True, null=True)
    is_type_umbrella = models.BooleanField(default=False)
    disbursement = models.FloatField(blank=True, null=True)
    disbursement_percentage = models.FloatField(blank=True, null=True)
    expenditure = models.FloatField(blank=True, null=True, verbose_name="Expenditure (PKRM)")
    expenditure_percentage = models.FloatField(blank=True, null=True)
    disbursement_total = models.FloatField(blank=True, null=True)
    expenditure_total = models.FloatField(blank=True, null=True, verbose_name="Total Cost (PKRM)")
    progress_planned_revised = models.DecimalField(default=0.0,max_digits = 5,decimal_places = 2,blank=True, null=True)
    disbursement_target = models.FloatField(blank=True, null=True)
    template = models.IntegerField(blank=True, null=True)
    disbursement_usd = models.FloatField(blank=True, null=True)
    name_short = models.CharField(max_length=255, blank=True, null=True)
    consultant_name = models.CharField(max_length=255, blank=True, null=True,verbose_name="Company")
    category_code = models.CharField(max_length=255, blank=True, null=True)

    contract_status_types = (
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('In Progress', 'In Progress'),
    )

    contract_status = models.CharField(max_length=255, blank=True, null=True, choices=contract_status_types,
                                       verbose_name="Contract Status")
    project_remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")

    @property
    def project_label(self):
        return str(self.code)+" / "+str(self.name)

    def save(self, *args, **kwargs):
        if self.serial_number is None or len(self.serial_number) < 1:
            from project.utils.SerialNumber import getSerialNumber
            self.serial_number = getSerialNumber()
      
        if self.city != self.organization.city:
            self.city = self.organization.city
            self.region = self.organization.region
      

        from project.utils.SerialNumber import getProjectRefencenNumber
        self.reference_number = getProjectRefencenNumber(self)

        super(QuillProject, self).save(*args, **kwargs)


    class params:
        db = 'quill_bcms'
    class Meta:
        managed = False
        unique_together = (('code','organization',))
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        db_table = 'pro_projects'

    def __str__(self):
        return str(self.project_label)
