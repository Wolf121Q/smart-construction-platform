from django.contrib import admin
from organization.models import Type
from utils.IP import get_client_ip
from django.utils.safestring import mark_safe
# Register your submodels here.

class TypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code','status','created_by','updated_by', 'created_on', 'updated_on')
    list_filter = ('status',)
    readonly_fields = ["created_on","updated_on","created_by","updated_by"]
    exclude = ("ip","created_by","updated_by")
    #fields = ('name', 'image', 'description')

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'name', 'code','status','created_on', 'updated_on'
                ),
            }
        ),
    )
    search_fields = ('name','code','status', 'created_on', 'updated_on')
    ordering = ('name','code','status', 'created_on', 'updated_on')


    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False


    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            # Only set added_by during the first save.
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        obj.ip = get_client_ip(request)
        super().save_model(request, obj, form, change)

admin.site.register(Type, TypeAdmin)