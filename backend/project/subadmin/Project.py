from django.contrib import admin
from django import forms
from project.models import Project
from utils.IP import get_client_ip
from core.models import SystemStatus
from core.models import User,Group
from django.contrib.admin.widgets import FilteredSelectMultiple
from vendor_company.models import VendorCompany
from django.db.models import F


# Register your submodels here.

class ProjectForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(queryset=User.objects.filter(is_active = True),required=False,widget=FilteredSelectMultiple("users",is_stacked=False,attrs={'rows': 5, 'class': 'input-2xlarge', 'style': 'width: 99% !important; resize: vertical !important;'}))
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(),widget=FilteredSelectMultiple("groups", is_stacked=False,attrs={'rows': 5, 'class': 'input-2xlarge', 'style': 'width: 99% !important; resize: vertical !important;'}))
    class Meta:
        model = Project
        exclude = ()

class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm
    list_display = ('name', 'code','city','organization','contract_status','created_by','updated_by', 'created_on', 'updated_on')
    list_filter = ('contract_status','organization')
    readonly_fields = ["region","city","type","created_on","updated_on","created_by","updated_by"]
    exclude = ("ip","created_by","updated_by")
    #fields = ('name', 'image', 'description')

    fieldsets = (
        ('Organization Info', {
            'fields': (('region','city','type'),(('organization')),'thumbnail')
        }),
        ('Project Info', {
            'fields': (('name','code'),('progress_actual','progress_planned'),('contractor','contract_status','expenditure_total'), 'category', 'status','start_date', 'end_date', 'project_remarks')
        }),
        ('User & Groups Info', {
            'fields': (('users', 'groups'))
        }),
    )
    search_fields = ('name','code','contract_status', 'created_on', 'updated_on')
    ordering = ('name','code','contract_status', 'created_on', 'updated_on')


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
            
        if db_field.name == "status":
            kwargs["queryset"] = SystemStatus.objects.filter(parent__system_code__in =['system_status_project_status'])               #kwargs['disabled'] = True

        if db_field.name == "contractor":
            qs = VendorCompany.objects.filter().annotate(city_ordering=F('city__tree_id'), city_lft=F('city__lft'))
            kwargs["queryset"] = qs.order_by('city_ordering', 'city_lft')
    
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            # Only set added_by during the first save.
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        obj.ip = get_client_ip(request)
        
        super().save_model(request, obj, form, change)
     
        if obj.region is None and obj.city is None:
            obj.region = obj.organization.region
            obj.city = obj.organization.city
        
        super().save_model(request, obj, form, change)

admin.site.register(Project, ProjectAdmin)