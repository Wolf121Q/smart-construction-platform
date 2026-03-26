from django.contrib import admin
from core.submodels.SystemType import SystemType
from utils.IP import get_client_ip
from dashboard.models import OrganizationChart


class OrganizationChartAdmin(admin.ModelAdmin):
    list_display_links = None
    change_list_template = 'organization_chart.html'

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
    ordering = ('name','code','contract_status', 'created_on', 'updated_on')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        ### ORGANIZATIONAL HIERARCHY ###
        type_organization = SystemType.objects.filter(system_code = request.user.type.system_code).first().get_descendants(include_self=True)
        parent_type_organization = SystemType.objects.filter(system_code = request.user.type.system_code).first().parent
        if type_organization and parent_type_organization:
            organization_data_list = [[x.parent.system_code,x.system_code] for x in type_organization]
            organization_nodes = [{'id':x.system_code,'title':x.name,'name': x.name} for x in type_organization]
            organization_nodes.insert(0, {'id':parent_type_organization.system_code,'title':parent_type_organization.name,'name': parent_type_organization.name})
            extra_context['organization_data_list'] = organization_data_list
            extra_context['organization_nodes'] = organization_nodes
        
        else:
            return "Hierarchy Not Defined"
        return super(OrganizationChartAdmin, self).changelist_view(request, extra_context=extra_context)
   

    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False
 
    # This will help you to disable delete functionaliyt
    def has_add_permission(self, request, obj=None):
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

admin.site.register(OrganizationChart,OrganizationChartAdmin)
