from django.contrib import admin
from utils.IP import get_client_ip
from vendor_company.models import VendorCompany
from django.contrib.admin import SimpleListFilter

class CityFilter(SimpleListFilter):
    title = 'Station' # or use _('country') for translated title
    parameter_name = 'city_id'

    def lookups(self, request, model_admin):
        # statuses = set([c.status for c in model_admin.model.objects.order_by('status__system_code').distinct('status__system_code')])
        cities =  set([c.city for c in model_admin.model.objects.order_by('city__code').distinct('city__code')])
        return [(c.id, c.name) for c in cities if c]
    def queryset(self, request, queryset):

        if self.value():
            return queryset.filter(city_id__exact=self.value())

class VendorCompanyAdmin(admin.ModelAdmin):
    list_display = ('name_of_company','get_city','code','status', 'created_on', 'updated_on')
    list_filter = (CityFilter,)
    readonly_fields = ["created_on","updated_on"]
    exclude = ("ip","created_by","updated_by")

    def get_city(self, obj):
        if obj.city:
            return obj.city
        return ""
    get_city.short_description = 'Station'


    #fields = ('name', 'image', 'description')

    # add_fieldsets = (
    #     (
    #         None,
    #         {
    #             'classes': ('wide',),
    #             'fields': (
    #                 'name', 'code','status','created_on', 'updated_on'
    #             ),
    #         }
    #     ),
    # )
    #search_fields = ('name','code','status', 'created_on', 'updated_on')
    #ordering = ('name','code','status', 'created_on', 'updated_on')

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "type":
    #         kwargs["queryset"] = VendorAttachmentType.objects.filter(code='vendor_contractor',status = 'active')
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False
    # def has_add_permission(self, request):
    #     if request.user.type.code == "system_type_vendor_type_contractor":
    #         return True
    #     else:
    #         return False

    # def has_change_permission(self, request, obj=None):
    #     if request.user.type.code == "system_type_vendor_type_contractor":
    #         return True
    #     else:
    #         return False

    # def has_view_permission(self, request, obj=None):
    #     if request.user.type.code == "system_type_vendor_type_contractor":
    #         return True
    #     else:
    #         return False

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            # Only set added_by during the first save.
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        obj.ip = get_client_ip(request)
        super().save_model(request, obj, form, change)
      
admin.site.register(VendorCompany, VendorCompanyAdmin)

    