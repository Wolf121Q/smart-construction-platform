from django.contrib import admin
from django import forms
from django.db import models
from project.models import TaskType
from utils.IP import get_client_ip
from django.utils.safestring import mark_safe
# Register your submodels here.


class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code','created_by','updated_by', 'created_on', 'updated_on')
    # list_filter = ('contract_status',)
    readonly_fields = ["created_on","updated_on","created_by","updated_by"]
    exclude = ("ip","created_by","updated_by")
    #fields = ('name', 'image', 'description')

    fieldsets = (
        (('Type Details'), {'fields': (('name', 'code','system_code'),('color','type','status'),'created_on','updated_on')}),
    )
    
    search_fields = ('name','code', 'created_on', 'updated_on')
    ordering = ('name','code', 'created_on', 'updated_on')


    def get_queryset(self, request):
        qs = super(TaskTypeAdmin, self).get_queryset(request)
        # if request.user.is_superuser:
        #     return qs
        return qs.filter(parent__system_code__in =['system_status_task_status'])

    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return True


    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            # Only set added_by during the first save.
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        obj.ip = get_client_ip(request)
        super().save_model(request, obj, form, change)

admin.site.register(TaskType, TaskTypeAdmin)