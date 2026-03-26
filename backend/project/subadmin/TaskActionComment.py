from django.contrib import admin
from project.models import TaskActionComment
from utils.IP import get_client_ip

class TaskActionCommentAdmin(admin.ModelAdmin):
    # form = ProjectForm
    # list_display = ('project', 'status','type','start_time','end_time', 'created_on', 'updated_on')
    # list_filter = ('project',)
    # readonly_fields = ["created_on","updated_on","created_by","updated_by"]
    # exclude = ("ip","created_by","updated_by")
    # #fields = ('name', 'image', 'description')
    #
    # # fieldsets = (
    # #     ('User & Groups Info', {
    # #         'fields': (('users', 'groups'))
    # #     }),
    # #     ('Organization Info', {
    # #         'fields': (('region','city','type'),('organization','thumbnail'))
    # #     }),
    # #     ('Project Info', {
    # #         'fields': (('name','code'), ('consultant_name', 'contractor_name', 'contract_status'), 'ca_no', 'category', 'status', ('start_date', 'end_date'), 'project_remarks')
    # #     }),
    # # )
    # search_fields = ('name','code','contract_status', 'created_on', 'updated_on')
    # ordering = ('name','code','contract_status', 'created_on', 'updated_on')


    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    # def save_model(self, request, obj, form, change):
    #     if not obj.created_by:
    #         # Only set added_by during the first save.
    #         obj.created_by = request.user
    #     else:
    #         obj.updated_by = request.user
    #     obj.ip = get_client_ip(request)
    #     super().save_model(request, obj, form, change)

admin.site.register(TaskActionComment, TaskActionCommentAdmin)