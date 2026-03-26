from django.contrib import admin
from core.models import SystemStatus
from dashboard.models import Report
#from daterange_filter.filter import DateRangeFilter
from utils.IP import get_client_ip
from dashboard.utils.generateReport import generate_project_report_pdf
from daterange_filter.filter import DateRangeFilter


class ReportAdmin(admin.ModelAdmin):
    list_display_links = None
    change_list_template = 'admin/change_list.html'
    list_display = ('region','city','organization','code','name','consultant_name','contractor_name','created_on','created_by','updated_on','updated_by')
    list_filter = ('contract_status',('created_on', DateRangeFilter))
    readonly_fields = ["region","city","type","created_on","updated_on","created_by","updated_by"]
    exclude = ("ip","created_by","updated_by")
    actions = [generate_project_report_pdf,]

    #fields = ('name', 'image', 'description')

    fieldsets = (
        ('User & Groups Info', {
            'fields': (('users', 'groups'))
        }),
        ('Organization Info', {
            'fields': (('region','city','type'),('organization','thumbnail'))
        }),
        ('Project Info', {
            'fields': (('name','code'), ('consultant_name', 'contractor_name', 'contract_status','expenditure_total'), 'category', 'status','start_date', 'end_date', 'project_remarks')
        }),
    )
    search_fields = ('name','code','contract_status', 'created_on', 'updated_on')
    ordering = ('name','code','contract_status', 'created_on', 'updated_on')


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
            
        if db_field.name == "status":
            kwargs["queryset"] = SystemStatus.objects.filter(parent__system_code__in =['system_status_project_status'])               #kwargs['disabled'] = True
    
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser == 0:
            return True
        else:
            return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser == 0:
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

admin.site.register(Report,ReportAdmin)
