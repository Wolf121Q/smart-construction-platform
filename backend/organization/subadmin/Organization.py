from django.contrib import admin
from organization.models import Organization
from utils.IP import get_client_ip
from django.utils.safestring import mark_safe
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from core.models import User,Group

# Register your submodels here.
class OrganizationForm(forms.ModelForm):
    # groups = forms.ModelChoiceField(queryset=Group.objects.all(),widget=ModelSelect2Widget(model=Group,search_fields=["name__icontains",],attrs={ 'data-html': True,'data-minimum-input-length': 0}),required=True)
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(),required=False,widget=FilteredSelectMultiple("users", is_stacked=False,attrs={'rows': 5, 'class': 'input-2xlarge', 'style': 'width: 99% !important; resize: vertical !important;'}))
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(),required=False,widget=FilteredSelectMultiple("groups", is_stacked=False,attrs={'rows': 5, 'class': 'input-2xlarge', 'style': 'width: 99% !important; resize: vertical !important;'}))
    
    class Meta:
        model = Organization
        fields = '__all__'


class OrganizationAdmin(admin.ModelAdmin):
    form = OrganizationForm
    list_display = ('name', 'code','city','region','status','created_by','updated_by', 'created_on', 'updated_on')
    list_filter = ('status',)
    readonly_fields = ["created_on","updated_on","created_by","updated_by"]
    exclude = ("ip","created_by","updated_by")
    #fields = ('name', 'image', 'description')

    fieldsets = (
        ('Geo Info', {
            'fields': (('region','city'))
        }),
        (('Organization Details'), {'fields': ('name', 'code','type','status','created_on', 'updated_on')}),
        (('Contact Details'), {'fields': ('phone','fax','email')}),
        (('Address'), {'fields': ('address_1','address_2','zipcode')}),
        (('Description'), {'fields': ('description',)}),
        ('User & Groups Info', {
            'fields': (('users', 'groups'))
        }),
    )
    
    
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

admin.site.register(Organization, OrganizationAdmin)