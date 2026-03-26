from django import forms
from django.db.models import Q

from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib import admin
from core.models import Role,RoleExtra,Permission,SystemType,SystemStatus
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from utils.IP import get_client_ip
csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())

admin.site.unregister(Group)


class RoleExtraInline(admin.StackedInline):
    model = RoleExtra
    exclude = ('ip','created_by','updated_by',)
    # This will help you to disable delete functionaliyt

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == "type":
            kwargs["queryset"] = SystemType.objects.filter(status='active', parent__system_code__in=['system_type_core_user_type'])  # kwargs['disabled'] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



    def has_delete_permission(self, request, obj=None):
        return False


class RoleForm(forms.ModelForm):

    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.exclude(Q(content_type_id__in=[1,4,5,6,7]) | Q(codename__startswith='delete_') | Q(codename__contains='historical')),widget=FilteredSelectMultiple("Permissions", is_stacked=False,attrs={'rows': 5, 'class': 'input-2xlarge', 'style': 'width: 99% !important; resize: vertical !important;'}))
    class Meta:
        model = Role
        exclude = ('created_by', 'updated_by')


    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/admin/jsi18n',)


class RoleAdmin(admin.ModelAdmin):
    form = RoleForm
    list_display = ('name','get_description')

    fieldsets = (
        ('', {'fields': ('name',)}),
        ('Permissions', {'fields': ('permissions',)}),
    )
    #list_filter = ('core_role_roleextra__related',)
    #readonly_fields = ["created_on","updated_on","created_by","updated_by"]
    #fields = ('name', 'image', 'description')
    filter_horizontal = ('permissions',)
    inlines = [
        RoleExtraInline,
    ]

    search_fields = ('name',)
    #ordering = ('title','status' , 'created_on')


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
            return True
        else:
            return False

    def has_view_permission(self, request, obj=None):
        if request.user.type.code == "system_type_user_developer_admin":
            return True
        else:
            return False

    def save_formset(self, request, form, formset, change):
        formset.save()
        for form in formset.forms:
            instance_meta = str(form.instance._meta)
            instance_name = instance_meta.rsplit('.', 1)[1].lower()

            if  instance_name == "roleextra":
                if not form.instance.created_by:
                    # Only set added_by during the first save.
                    form.instance.created_by = request.user
                else:
                    form.instance.updated_by = request.user
                form.instance.ip = get_client_ip(request)
                form.instance.save()

    def get_description(self, obj):
        roleextra = RoleExtra.objects.get(role=obj.id)
        return roleextra.description

    get_description.short_description = 'Description'

admin.site.register(Role, RoleAdmin)