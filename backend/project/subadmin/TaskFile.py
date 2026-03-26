from django.contrib import admin
from django import forms
from django.db import models
from searchableselect.widgets import SearchableSelect
from project.models import TaskFile
from utils.IP import get_client_ip
from django.utils.safestring import mark_safe
# Register your submodels here.


class TaskFileAdmin(admin.ModelAdmin):
    list_display = ('filename', 'created_by', 'updated_by', 'created_on', 'updated_on')
    # list_filter = ('contract_status',)
    readonly_fields = ["created_on","updated_on","created_by","updated_by"]
    exclude = ("ip", "created_by", "updated_by")
    #fields = ('name', 'image', 'description')

    # fieldsets = (
    #     ('Task Info', {
    #         'fields': (('project', 'name', 'code'), ('start_date','end_date', 'status'))
    #     }),
    # )
    search_fields = ('filename', 'created_on', 'updated_on')
    ordering = ('filename', 'created_on', 'updated_on')


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

admin.site.register(TaskFile, TaskFileAdmin)