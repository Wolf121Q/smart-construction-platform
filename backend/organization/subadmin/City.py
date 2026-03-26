from django.contrib import admin
from organization.models import City
from utils.IP import get_client_ip
from django.utils.safestring import mark_safe
from core.models import User,Group,RoleExtra
from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

# Register your submodels here.
class CityForm(forms.ModelForm):
    # groups = forms.ModelChoiceField(queryset=Group.objects.all(),widget=ModelSelect2Widget(model=Group,search_fields=["name__icontains",],attrs={ 'data-html': True,'data-minimum-input-length': 0}),required=True)
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(),required=False,widget=FilteredSelectMultiple("users", is_stacked=False,attrs={'rows': 5, 'class': 'input-2xlarge', 'style': 'width: 99% !important; resize: vertical !important;'}))
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(),required=False,widget=FilteredSelectMultiple("groups", is_stacked=False,attrs={'rows': 5, 'class': 'input-2xlarge', 'style': 'width: 99% !important; resize: vertical !important;'}))
    
    class Meta:
        model = City
        fields = '__all__'

# class CityAdmin(DraggableMPTTAdmin):
#     mptt_indent_field = "name"
#     #list_display_links = ('indented_name',)
#     form = CityForm
#     list_display = ('name', 'code', 'status', 'created_on', 'updated_on')
#     list_filter = ('status',)
#     readonly_fields = ["created_on","updated_on","created_by","updated_by"]
#     exclude = ("ip","created_by","updated_by")
#     #fields = ('name', 'image', 'description')
#
#     fieldsets = (
#         ('User & Groups Info', {
#             'fields': (('users', 'groups'))
#         }),
#         ('Geo Info', {
#             'fields': (('region',))
#         }),
#         (('City Details'), {'fields': ('name', 'code','status','created_on', 'updated_on')}),
#     )
#
#     search_fields = ('name','code','status', 'created_on', 'updated_on')
#     ordering = ('name','code','status', 'created_on', 'updated_on')
#
#     # This will help you to disable delete functionaliyt
#     def has_delete_permission(self, request, obj=None):
#         return False
#
#     def has_add_permission(self, request):
#         if request.user.type.code == "super_admin_user":
#             return True
#     def has_change_permission(self, request, obj=None):
#         if request.user.type.code == "super_admin_user":
#             return True
#         else:
#             return True
#
#     def has_view_permission(self, request, obj=None):
#         if request.user.type.code == "super_admin_user":
#             return True
#
#     def save_model(self, request, obj, form, change):
#         if not obj.created_by:
#             # Only set added_by during the first save.
#             obj.created_by = request.user
#         else:
#             obj.updated_by = request.user
#         obj.ip = get_client_ip(request)
#         super().save_model(request, obj, form, change)
#
# admin.site.register(City, CityAdmin)



class CityAdmin(DraggableMPTTAdmin):
    form = CityForm
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title')
    list_display_links = ('indented_title',)
    list_filter = ('parent__name',)
    readonly_fields = ["created_on", "updated_on"]
    # fields = ('name', 'image', 'description')

    fieldsets = (
        ('Geo Info', {
            'fields': (('region',))
        }),
        (('City Details'), {'fields': ('name', 'code','status','created_on', 'updated_on')}),

        ('User & Groups Info', {
            'fields': (('users', 'groups'))
        }),
    )
    
    search_fields = ('name', 'created_on')

    # ordering = ('title','status' , 'created_on')


    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return True
    def has_change_permission(self, request, obj=None):
        if request.user.type.code == "super_admin_user":
            return True
        else:
            return True

    def has_view_permission(self, request, obj=None):
        if request.user.type.code == "super_admin_user":
            return True
        elif request.user.type.code == "system_user":
            return True
        else:
            return True

admin.site.register(City, CityAdmin)