from django.contrib import admin
from core.models import UserType
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from utils.IP import get_client_ip

csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())




class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'created_on', 'updated_on')
    list_filter = ('status',)
    readonly_fields = ["created_on", "updated_on"]
    exclude = ('ip',)
    # fields = ('name', 'image', 'description')

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'name', 'code', 'status', 'created_on', 'updated_on'
                ),
            }
        ),
    )
    search_fields = ('name', 'code', 'status', 'created_on', 'updated_on')
    ordering = ('name', 'code', 'status', 'created_on', 'updated_on')


    def get_queryset(self, request):
        qs = super(UserTypeAdmin, self).get_queryset(request).filter(parent__system_code = "system_type_core_user_type")
        return qs

    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        if request.user.type.code == "system_type_core_user_super_admin":
            return False
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.type.code == "system_type_core_user_super_admin":
            return False
        else:
            return False

    def has_view_permission(self, request, obj=None):
        if request.user.type.code == "system_type_core_user_super_admin":
            return True
        else:
            return False

    def save_model(self, request, obj, form, change):
        # if not obj.created_by:
        #     # Only set added_by during the first save.
        #     #obj.created_by = request.user
        # else:
        #     #obj.updated_by = request.user
        obj.ip = get_client_ip(request)
        super().save_model(request, obj, form, change)


admin.site.register(UserType, UserTypeAdmin)