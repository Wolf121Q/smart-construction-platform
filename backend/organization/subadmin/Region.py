from django.contrib import admin
from organization.models import Region
from utils.IP import get_client_ip
from django.utils.safestring import mark_safe
#from searchableselect.widgets import SearchableSelect
from django import forms
from django.db import models
from core.models import User,Group,RoleExtra
from django.db.models import Subquery
from django import forms
from django_select2.forms import ModelSelect2Widget,HeavySelect2Widget
from django.contrib.admin.widgets import FilteredSelectMultiple

# Register your submodels here.

# class RegionForm(forms.ModelForm):
#     class Meta:
#         model = Region
#         exclude = ()
#         widgets = {
#             'users': SearchableSelect(model='core.User', search_field='username', many=True, limit=10),
#             'groups': SearchableSelect(model='auth.Group', search_field='name', many=True, limit=10),
#         }

class RegionForm(forms.ModelForm):
    # groups = forms.ModelChoiceField(queryset=Group.objects.all(),widget=ModelSelect2Widget(model=Group,search_fields=["name__icontains",],attrs={ 'data-html': True,'data-minimum-input-length': 0}),required=True)
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(),required=False,widget=FilteredSelectMultiple("users",is_stacked=False,attrs={'rows': 5, 'class': 'input-2xlarge', 'style': 'width: 99% !important; resize: vertical !important;'}))
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(),required=False,widget=FilteredSelectMultiple("groups",is_stacked=False,attrs={'rows': 5, 'class': 'input-2xlarge', 'style': 'width: 99% !important; resize: vertical !important;'}))
    
    class Meta:
        model = Region
        fields = '__all__'


class RegionAdmin(admin.ModelAdmin):
    form = RegionForm
    list_display = ('name', 'code','status','created_by','updated_by', 'created_on', 'updated_on')
    list_filter = ('status',)
    readonly_fields = ["created_on","updated_on","created_by","updated_by"]
    exclude = ("ip","created_by","updated_by")
   
    
    
    #fields = ('name', 'image', 'description')
    #autocomplete_fields = ['groups']
    # fieldsets = (('None', {'fields': (('name','code'),('ordering','status'),'groups')}),)

    fieldsets = (
        (('Region Details'), {'fields': (('name', 'code','status'),'created_on','updated_on')}),
        ('User & Groups Info', {
            'fields': (('users', 'groups'))
        }),
    )
    
    
    
    
    
    
    # add_fieldsets = (
    #     (
    #         ('User & Groups Info', {
    #         'fields': (('users', 'groups'))
    #         }),
    #         (None,
    #         {
    #             'classes': ('wide',),
    #             'fields': (
    #                 'name', 'code','status','created_on', 'updated_on'
    #             ),
    #         }),
    #     ),
    # )
    search_fields = ('name','code','status', 'created_on', 'updated_on')
    ordering = ('name','code','status', 'created_on', 'updated_on')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
            
        if db_field.name == "users":
            kwargs["queryset"] = User.objects.all()#User.objects.filter(type__system_code = 'system_type_user_region')
            #kwargs['disabled'] = True
            
        if db_field.name == 'groups':
            kwargs["queryset"] = Group.objects.filter(name = RoleExtra.objects.filter(system_code = 'system_type_user_type_region').first().role.name)
                #kwargs['disabled'] = True
            # except:
            #     kwargs["queryset"] = Group.objects.all()
    
        return super().formfield_for_manytomany(db_field, request, **kwargs)

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

admin.site.register(Region, RegionAdmin)