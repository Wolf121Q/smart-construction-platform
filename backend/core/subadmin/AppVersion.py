from django.contrib import admin
from core.models import AppVersion
from utils.IP import get_client_ip
from django.utils.safestring import mark_safe
# Register your submodels here.


class AppVersionAdmin(admin.ModelAdmin):
    list_display = ('name', 'type','version','created_by','updated_by', 'created_on', 'updated_on')
    # list_filter = ('contract_status',)
    readonly_fields = ["created_on","updated_on","created_by","updated_by"]
    exclude = ("ip","created_by","updated_by")
    #fields = ('name', 'image', 'description')

    # fieldsets = (
    #     ('Task Info', {
    #         'fields': (('project', 'name', 'code'), ('start_date','end_date', 'status'))
    #     }),
    # )
    search_fields = ('name', 'type','version', 'created_on', 'updated_on')
    ordering = ('name', 'type','version', 'created_on', 'updated_on')


    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request):
        if request.user.type.code == "system_type_core_user_type_android_developer":
            return True
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.type.code == "system_type_core_user_type_android_developer":
            return True
        else:
            return False

    def has_view_permission(self, request, obj=None):
        if request.user.type.code == "system_type_core_user_type_android_developer":
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

admin.site.register(AppVersion, AppVersionAdmin)