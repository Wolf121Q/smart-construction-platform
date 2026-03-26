from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from core.models import SystemStatus
from django.utils.safestring import mark_safe
from django.db.models import Q
from daterange_filter.filter import DateRangeFilter
from project.models import TaskAction,TaskActionTimeLine,Project
from datetime import datetime

# sdfsdf
class StatusFilter(SimpleListFilter):
    title = 'Status' # or use _('country') for translated title
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        statuses = set([c.status for c in model_admin.model.objects.order_by('status__system_code').distinct('status__system_code')])
        return [(c.id, c.name) for c in statuses]

    def queryset(self, request, queryset):

        if self.value():
            return queryset.filter(status__id__exact=self.value())

class CategoryFilter(SimpleListFilter):
    title = 'Category' # or use _('country') for translated title
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        categories = set([c.category for c in model_admin.model.objects.filter(category__isnull=False).order_by('category__system_code').distinct('category__system_code')])
        if categories is not None:
            return [(c.id, c.name) for c in categories]
        return None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category_id = self.value())

class CityFilter(SimpleListFilter):
    title = 'City' # or use _('country') for translated title
    parameter_name = 'project__city_id'

    def lookups(self, request, model_admin):
        cities = set([c.project.city for c in model_admin.model.objects.filter(project__city__isnull=False).order_by('project__city__code').distinct('project__city__code')])
        if cities is not None:
            return [(c.id, c.name) for c in cities]
        return None
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(project__city__id__exact=self.value())

class RegionFilter(SimpleListFilter):
    title = 'Region' # or use _('country') for translated title
    parameter_name = 'project__region_id'
  
    def lookups(self, request, model_admin):
        regions = set([c.project.region for c in model_admin.model.objects.filter(project__region__isnull=False).order_by('project__region__code').distinct('project__region__code')])
        if regions is not None:
            return [(c.id, c.name) for c in regions]
        return None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(project__region__id__exact=self.value())

class InspectionFilter(SimpleListFilter):
    title = 'Flag Type' # or use _('country') for translated title
    parameter_name = 'status__parent_id'

    def lookups(self, request, model_admin):
        regions = set([c.status.parent for c in model_admin.model.objects.filter(status__parent__isnull=False).order_by('status__parent__code').distinct('status__parent__code')])
        if regions is not None:
            return [(c.id, c.name) for c in regions]
        return None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status__parent__id = self.value())

class MaterialFlagsFilter(SimpleListFilter):
    title = 'Material Flags' # or use _('country') for translated title
    parameter_name = 'status_id'

    def lookups(self, request, model_admin):
        filters = {}
        filters['status__isnull'] = False
        filters['status__parent__system_code'] = "system_status_task_status_material"
        filter_q = Q(**filters)
        flags = set([c.status for c in model_admin.model.objects.filter(filter_q).order_by('status__code').distinct('status__code')])
        if flags is not None:
            return [(c.id, c.name) for c in flags]
        return None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status__id__exact = self.value())

class InspectionFlagsFilter(SimpleListFilter):
    title = 'Inspection Flags' # or use _('country') for translated title
    parameter_name = 'status_id'

    def lookups(self, request, model_admin):
        filters = {}
        filters['status__isnull'] = False
        filters['status__parent__system_code'] = "system_status_task_status_inspection"
        filter_q = Q(**filters)
        flags = set([c.status for c in model_admin.model.objects.filter(filter_q).order_by('status__code').distinct('status__code')])
        if flags is not None:
            return [(c.id, c.name) for c in flags]
        return None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status__id__exact = self.value())

class TaskActionAdmin(admin.ModelAdmin):
    list_per_page = 10
    change_form_template = 'admin/change_form.html'
    change_list_template = 'task_action_templates/change_list.html'
    list_display = ('serial_number','ca_ref_no','get_flag','flag_parent_type','type_of_work','created_by','created_on','get_obsn','action_btns')
    fields = ['description']
    ordering = ['-created_on']
    list_filter = (('created_on',DateRangeFilter),RegionFilter,CityFilter,InspectionFilter,MaterialFlagsFilter,InspectionFlagsFilter)
    search_fields = ['serial_number','project__reference_number','status__name','created_by__email','updated_by__email','task__name','status__parent__name']
    date_hierarchy = 'created_on'


    """ Calculated Fields """    
    def ca_ref_no(self, obj):
        return obj.project.reference_number

    ca_ref_no.short_description = 'CA REF#'

    def get_flag(self, obj,inspection_id = None,flag_id = None):
        return mark_safe('<i class="fa fa-flag" style="color:{flag_color};font-size:25px"></i>'.format(flag_color = obj.status.color))   
    
    # get_flag.admin_order_field  = 'parent_project_taskactions'  #Allows column order sorting
    get_flag.short_description = 'Flags'  #Renames column head

    def flag_parent_type(self, obj):
        return obj.status.parent.name
    
    flag_parent_type.short_description = 'INSPECTION TYPE'


    def type_of_work(self, obj):
        return obj.task

    type_of_work.short_description = 'TYPE OF WORK'
   
    def action_btns(self, obj):
        return mark_safe("<a href ='javascript:void(0);' onclick=ChatBoxApi.ShowChatBox('{task_action_id}','{project_ref_no}') class='btn-outline-info border-0 mr-2'><i class='far fa-comment-dots text-130'>\
            </i></a><a type='button' onclick=ChatBoxApi.task_action_first_attachment('{task_action_id}') class='btn-outline-info border-0'><i class='fas fa-paperclip text-130'></i></a>".format(task_action_id = obj.id,project_ref_no = obj.project.reference_number.replace(' ', '_')))
    
    action_btns.short_description = 'ACTION'

    def get_obsn(self, obj):
        return mark_safe('<a onclick="DashboardApi.obsnModal(\'{desc}\')" href="javascript:void(0);" class="btn btn-bold btn-outline-primary btn-h-primary fs--outline border-0 btn-a-primary radius-0 px-35 mb-1" data-toggle="tooltip" data-original-title="Flag Detail">Show Obsn</a>'.format(
                desc = str(obj.description),
        ))
    get_obsn.admin_order_field  = 'Description'  #Allows column order sorting
    get_obsn.short_description = ''  #Renames column head
    
    def changelist_view(self, request, extra_context=None):
        queryset = TaskAction.objects.filter()
        insp_flag_filtered_query_set = queryset.filter(status__parent__system_code = "system_status_task_status_inspection")
        mat_flag_filtered_query_set = queryset.filter(status__parent__system_code = "system_status_task_status_material")
        extra_context = {
             'mat_flag_filtered_query_set': self.getFlagStats(mat_flag_filtered_query_set,"material"),
             'ins_flag_filtered_query_set': self.getFlagStats(insp_flag_filtered_query_set,"inspection"),
        }
        extra_context['total_projects'] = Project.objects.filter().count()
        return super().changelist_view(request, extra_context=extra_context)

    
    def getFlagStats(self,flag_qs,flag_type=None):
        data_list = []
        if flag_type == "inspection":
            flags = SystemStatus.objects.filter(parent__system_code = "system_status_task_status_inspection")
        else:
            flags = SystemStatus.objects.filter(parent__system_code = "system_status_task_status_material")
        for entry in flags:
            entry_list = []
            entry_list.append(entry.color)
            entry_list.append(flag_qs.filter(status_id = str(entry.id)).count())
            entry_list.append(flag_qs.filter(status_id = entry.id,end_time__isnull = False).count())
            data_list.append(entry_list)
        return data_list
 
   
    # # This will help you to disable delete functionaliyt
    def get_queryset(self, request):
        qs = self.model._default_manager.get_queryset()
        time_line_obj = TaskActionTimeLine.objects.filter(user_type = request.user.type).first()
        if time_line_obj:
            time_line = datetime.now() - time_line_obj.time_line
            qs = qs.filter(created_on__date__gte = time_line.date())
        else:
            qs = self.model._default_manager.get_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs.order_by('-created_on')
    
    
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

admin.site.register(TaskAction,TaskActionAdmin)
