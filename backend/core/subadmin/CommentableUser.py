from django.contrib import admin
from core.models import CommentableUserType
from utils.IP import get_client_ip

class CommentableUserTypeAdmin(admin.ModelAdmin):
    list_display = ('display_user_types','created_by','created_on','updated_by','updated_on')

    def display_user_types(self, obj):
        return ", ".join([str(user_type) for user_type in obj.user_types.all()])
    
    readonly_fields = ["created_on","updated_on",]
    exclude = ["created_by","updated_by","ip"]

    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
         if request.user.type.code == "system_type_user_developer_admin":
             return False
         else:
             return False
    
    def has_change_permission(self, request, obj=None):
         if request.user.type.code == "system_type_user_developer_admin":
             return False
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

admin.site.register(CommentableUserType, CommentableUserTypeAdmin)