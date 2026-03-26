from django.contrib import admin
from core.models import UserTypeHierarchy
from utils.IP import get_client_ip
from core.models import SystemType

class UserTypeHierarchyAdmin(admin.ModelAdmin):
    list_display = ('hierarchy_tree','status', 'created_by','created_on')
    readonly_fields = ["created_on","updated_on",]
    exclude = ["created_by","updated_by","ip"]
    # search_fields = ('name','code','status', 'created_on', 'updated_on')

    def hierarchy_tree(self, obj):
        return f'{obj.user_type.name} >> ({", ".join(user_type.name for user_type in obj.group_user_types.all())})'
    hierarchy_tree.short_description = "Hirerchy"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user_type":
            kwargs["queryset"] = SystemType.objects.filter(system_code = "system_type_core_user_type_organization_chart_ag",status="active").first().get_descendants(include_self=True)               #kwargs['disabled'] = True

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "group_user_types":
            kwargs["queryset"] = SystemType.objects.filter(system_code = "system_type_core_user_type_organization_chart_ag",status="active").first().get_descendants(include_self=True)             #kwargs['disabled'] = True
            #kwargs["queryset"] = Group.objects.filter(core_roleextras__type__code="system_type_core_user_super_admin")
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False
    
    # def has_add_permission(self, request):
    #     if request.user.type.code == "super_admin_user":
    #         return True
    #     else:
    #         return False
    #
    # def has_change_permission(self, request, obj=None):
    #     if request.user.type.code == "super_admin_user":
    #         return True
    #     else:
    #         return False
    #
    # def has_view_permission(self, request, obj=None):
    #     if request.user.type.code == "super_admin_user":
    #         return True
    #     else:
    #         return False

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            # Only set added_by during the first save.
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        obj.ip = get_client_ip(request)
        super().save_model(request, obj, form, change)

admin.site.register(UserTypeHierarchy, UserTypeHierarchyAdmin)