from django.db import models
import uuid
from core.models import SystemStatus,User
from organization.models import Region,City
from utils.Upload import Upload
from django.db.models.manager import EmptyManager
# from housing_society.models import Society

class VendorCompany(models.Manager):
    def get_queryset(self):
        return super(VendorCompany, self).get_queryset().filter()

class VendorCompany(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On")
    updated_on = models.DateTimeField(auto_now=True, verbose_name="Updated On")
    created_by = models.ForeignKey(User, null=True, blank=True,  verbose_name="Created By",  on_delete=EmptyManager,related_name="c_%(app_label)s_%(class)s_related",related_query_name="c_%(app_label)s_%(class)ss")
    updated_by = models.ForeignKey(User, null=True, blank=True,  verbose_name="Updated By", on_delete=EmptyManager,related_name="u_%(app_label)s_%(class)s_related",related_query_name="u_%(app_label)s_%(class)ss")
    user = models.OneToOneField(User, null=True, blank=True,  verbose_name="Vendor", on_delete=EmptyManager,related_name="v_%(app_label)s_%(class)s_related",related_query_name="v_%(app_label)s_%(class)ss")
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Address")
    name_of_company = models.CharField(max_length=100,blank = False,verbose_name="Company Name")
    company_reg_no = models.CharField(max_length=50,unique=True, null=True,blank=True, verbose_name="Company/Firm Registration No")
    # society = models.ForeignKey(Society, null=True, blank=True, verbose_name="Society", on_delete=models.CASCADE,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    phone = models.CharField(max_length=100,null=True,blank=True)
    phone_code = models.CharField(max_length=100, unique=False, null=True, blank=True)
    serial_number = models.CharField(max_length=100,unique=True,null=True, blank=True,verbose_name="Serial Number",editable=False)
    fax = models.CharField(max_length=20,unique=False)
    code = models.CharField(max_length=100,unique=False)
    email = models.CharField(max_length=100,unique=False)
    website = models.CharField(max_length=100,unique=False)
    description = models.TextField(null=True,blank=True)
    ntn = models.CharField(max_length=50,unique=True, null=True,blank=False, verbose_name="National Tax Number (NTN)")
    ntn_certificate_no = models.CharField(max_length=50,unique=False,null=True,blank=False, verbose_name="Certificate No")
    ntn_valid_upto = models.DateField(null=True,blank=False, verbose_name="Valid Upto")
    
    fbr_registration = models.CharField(max_length=50,unique=False, null=True,blank=False, verbose_name="FBR Registration")
    fbr_certificate_no = models.CharField(max_length=50,unique=False,null=True,blank=False, verbose_name="Certificate No")
    fbr_valid_upto = models.DateField(null=True,blank=False,verbose_name="Valid Upto")
    
    strn = models.CharField(max_length=50,unique=False, null=True,blank=True, verbose_name="Sales Tax Registration Number (STRN)")
    gst_no = models.CharField(max_length=50,unique=True, null=True,blank=True, verbose_name="GST No.")
    pec_reg_no = models.CharField(max_length=50,unique=True, null=True,blank=True, verbose_name="PEC Reg No")
    pec_category = models.CharField(max_length=50,unique=True, null=True,blank=True, verbose_name="PEC Category")

    # SHOULD BE FALSE
    established_on = models.DateField(null=True, verbose_name="Established In")
    prefix_consumerid = models.CharField(max_length=4, unique=False, verbose_name="Prefix ECommerce ID")

    region = models.ForeignKey(Region,null=True, blank=True, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    city = models.ForeignKey(City,null=True, blank=True, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")

    address_1 = models.CharField(max_length=100,null=True, blank=True)
    address_2 = models.CharField(max_length=100,null=True,blank=True)
    zipcode = models.CharField(max_length=10,null=True, blank=True)
    ownership = models.BooleanField(default=False,verbose_name="System Ownership",null=True,blank=True)
    logo = models.FileField(max_length=250,blank=True,null=True,upload_to=Upload)
   
    C_CATEGORY = (
        ("C-A", "C-A"),
        ("C-B", "C-B"),
        ("C-1", "C-1"),
        ("C-2", "C-2"),
        ("C-3", "C-3"),
        ("C-4", "C-4"),
        ("C-5", "C-5"),
        ("C-6", "C-6"),
        ("C-7", "C-7"),
    )
    category_applied = models.CharField(max_length=50,choices=C_CATEGORY , null=True,blank=True)

    remarks = models.TextField(null=True, blank=True, verbose_name="Remarks")
    status = models.ForeignKey(SystemStatus, null=True, blank=True,  verbose_name="Status", on_delete=EmptyManager,related_name="status_%(app_label)s_%(class)s_related",related_query_name="status_%(app_label)s_%(class)ss")
      
    @property
    def address(self):
        return self.address_1 + " " + self.address_2

    class Meta:
        unique_together = (('ntn', 'code',))
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        db_table = 'ven_companies'

    def __str__(self):
        if self.city:
            return f"{self.name_of_company} ({self.city.short_name})" 
        return f"{self.name_of_company}" 
























