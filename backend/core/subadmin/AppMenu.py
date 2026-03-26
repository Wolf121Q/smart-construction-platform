from django.contrib import admin
from django.utils.html import mark_safe
from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin
from core.models import AppMenu

class AppMenuAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title','show_icon')
    list_display_links = ('indented_title',)
    list_filter = ('parent__name',)
    readonly_fields = ["show_icon","created_on", "updated_on"]
    # fields = ('name', 'image', 'description')

    add_fieldsets = (
        (
            None,
            {
                'classes': ('inline',),
                'fields': (
                    'name', 'parent', 'created_on'
                ),
            }
        ),
    )
    search_fields = ('name', 'created_on')

    # ordering = ('title','status' , 'created_on')


    def show_icon(self, obj):
        if obj:
            return mark_safe('<i class="%s"></i>' % (obj.icon))
        else:
            return ""
    show_icon.short_description = 'icon'  #Renames column head

    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        if request.user.type.code == "system_type_user_developer_admin":
            return True
        else:
            return False

    def has_view_permission(self, request, obj=None):
        if request.user.type.code == "system_type_user_developer_admin":
            return True
        elif request.user.type.code == "system_user":
            return True
        else:
            return False

admin.site.register(AppMenu, AppMenuAdmin)