from django.contrib import admin
from django import forms
from django.db import models
from project.models import Task
from utils.IP import get_client_ip
from django.utils.safestring import mark_safe
from core.models import SystemStatus
# Register your submodels here.



class TaskAdmin(admin.ModelAdmin):
    # form = TaskAdminForm
    list_display = ('name', 'code','created_by','updated_by', 'created_on', 'updated_on')
    # list_filter = ('contract_status',)
    readonly_fields = ["created_on", "updated_on", "created_by", "updated_by"]
    exclude = ("ip", "created_by", "updated_by")
    #fields = ('name', 'image', 'description')
    autocomplete_fields = ['project',]


    fieldsets = (
        ('Task Info', {
            'fields': (('project', 'name', 'code'), ('start_date','end_date', 'status'))
        }),
        ('Description', {
            'fields': ('description',)
        }),
    )
    search_fields = ('name','code', 'created_on', 'updated_on')
    ordering = ('name','code', 'created_on', 'updated_on')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
            
        if db_field.name == "status":
            kwargs["queryset"] = SystemStatus.objects.filter(parent__system_code__in =['system_status_task_status_material','system_status_task_status_inspection'])
            #kwargs['disabled'] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
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

admin.site.register(Task, TaskAdmin)