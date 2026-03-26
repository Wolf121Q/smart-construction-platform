import traceback
from xml.etree.ElementInclude import include
from django.contrib import admin
from core.models import OrganizationHierarchy
from utils.IP import get_client_ip
from mptt.admin import DraggableMPTTAdmin
from core.models import SystemType
from django.utils.safestring import mark_safe

class OrganizationHierarchyAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title','name', 'code','status', 'created_on', 'updated_on')
    list_filter = ('status',)
    readonly_fields = ["created_on","updated_on"]
    exclude = ("ip","created_by","updated_by")
    #fields = ('name', 'image', 'description')

    fieldsets = (
        ('', {
            'fields': (('name','code','system_code','parent'),('color','status'))
        }),
    )
 
    search_fields = ('name','code','status', 'created_on', 'updated_on')
    ordering = ('name','code','status', 'created_on', 'updated_on')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
            
        if db_field.name == "parent":
            kwargs["queryset"] = SystemType.objects.filter(system_code="system_type_core_user_type_organization_chart").get_descendants(include_self=True).filter(status='active')
    
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(OrganizationHierarchyAdmin, self).get_queryset(request)
        return qs.get(system_code = 'system_type_core_user_type_organization_chart').get_descendants(include_self=False).filter(status='active')
        
        
        #.first().get_descendants(include_self=False).filter(status='active')

    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        if request.user.type.code == "system_type_user_developer_admin":
            return True
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.type.code == "system_type_user_developer_admin":
            return True
        else:
            return False

    def has_view_permission(self, request, obj=None):
        if request.user.type.code == "system_type_user_developer_admin":
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

admin.site.register(OrganizationHierarchy, OrganizationHierarchyAdmin)