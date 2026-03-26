from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from core.models import SystemStatus
from django.utils.safestring import mark_safe
from django.db.models import Q,Count,F
from daterange_filter.filter import DateRangeFilter
from project.models import TaskStatus,TaskFile,TaskAction,TaskActionTimeLine,Project,Organization
from django.urls import reverse
from dashboard.models import RectifiedFlag
from dashboard.utils.generateRectifiedReport import generate_project_report_pdf
from dashboard.utils.filterUserBasedQs import weekly_obsns_datefilter,filtered_qs_rolebased,filtered_region_rolebased,filtered_city_rolebased
from organization.models import City,Region
from dashboard.utils.flag_management import TaskActionManager
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta
from django.utils.timezone import now
from django import forms


class TimeSinceFilterForm(forms.Form):
    CHOICES = [
        ('', 'All flags'),
        ('1_week', _('1 week ago')),
        ('1_month', _('1 month ago')),
        ('3_months', _('3 months ago')),
        ('6_months', _('6 months ago')),
    ]
    
    time_since = forms.ChoiceField(choices=CHOICES, required=False)

class FlagFilterForm(forms.Form):
    flag_form_filter_field = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        # Extract the request or any other required data
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        # Get choices from a method
        self.fields['flag_form_filter_field'].choices = self.get_task_action_choices(request)

    def get_task_action_choices(self, request):
        # Retrieve distinct statuses of parent TaskActions
        task_action_manager = TaskActionManager(TaskAction,request)
        rectified_flags = task_action_manager.get_rectified_flags()
        # Retrieve parent IDs from the queryset
        parent_ids = rectified_flags.values_list('parent_id', flat=True).distinct()
        # Fetch parent instances based on the parent IDs
        parents = TaskAction.objects.filter(id__in=parent_ids)

        statuses = set([c.status for c in parents.order_by('status__code').distinct('status__code')])
        if statuses is not None:
            choices = [('', 'All Flags')]  # The empty string is used for the default option
            choices.extend([(c.id, f"{c.name} ({c.parent.name})") for c in statuses])
            return choices
        return [('', 'All Flags')] 



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
        


class ParentStatusFilter(admin.SimpleListFilter):
    title = 'Parent Flag'
    parameter_name = 'parent_status'

    def lookups(self, request, model_admin):
        # Retrieve distinct statuses of parent TaskActions
        task_action_manager = TaskActionManager(TaskAction,request)
        rectified_flags = task_action_manager.get_rectified_flags()
        # Retrieve parent IDs from the queryset
        parent_ids = rectified_flags.values_list('parent_id', flat=True).distinct()
        # Fetch parent instances based on the parent IDs
        parents = TaskAction.objects.filter(id__in=parent_ids)

        statuses = set([c.status for c in parents.order_by('status__code').distinct('status__code')])
        if statuses is not None:
            return [(c.id,f"{c.name} ({c.parent.name})") for c in statuses]
        return None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(parent__status=self.value())
        return queryset
    


class TimeAgoFilter(admin.SimpleListFilter):
    title = _('Rectified Since')
    parameter_name = 'time_ago'

    def lookups(self, request, model_admin):
        return (
            ('1_week', _('1 week ago')),
            ('1_month', _('1 month ago')),
            ('3_months', _('3 months ago')),
            ('6_months', _('6 months ago')),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            now_time = now()
            if value == '1_week':
                start_date = now_time - timedelta(weeks=1)
            elif value == '1_month':
                start_date = now_time - timedelta(days=30)
            elif value == '3_months':
                start_date = now_time - timedelta(days=90)
            elif value == '6_months':
                start_date = now_time - timedelta(days=180)
            else:
                return queryset

            return queryset.filter(created_on__gte=start_date)
        return queryset


class RectifiedFlagAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display_links = None
    list_max_show_all = 10000000000000000000000000
    change_form_template = 'admin/change_form.html'
    change_list_template = 'task_action_templates/rectified_flag_change_list.html'
    list_display = ['ca_ref_no','get_flag','get_description','created_by','created_on','action_btns']
    ordering = ['-created_on']
    list_filter = (('created_on',DateRangeFilter),TimeAgoFilter,InspectionFilter,RegionFilter,CityFilter,ParentStatusFilter,'project__organization')
    search_fields = ['serial_number','project__reference_number','status__name','created_by__email','updated_by__email','task__name','status__parent__name']
    fields = ['description','status']
    date_hierarchy = 'created_on'
    actions = [generate_project_report_pdf,]


    # Permission Based List Ammendment
    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        if 'dashboard.change_rectifiedflag' in request.user.get_group_permissions():
            if 'edit_flag' not in list_display:
                list_display.append('edit_flag',)
        else:
            if 'edit_flag' in list_display:
                list_display.remove('edit_flag')
        return list_display


    """ Calculated Fields """    
    def ca_ref_no(self, obj):
        return obj.project.reference_number

    ca_ref_no.short_description = 'CA REF#'

    def get_flag(self, obj,inspection_id = None,flag_id = None):
        if obj:
            rectified_flag = TaskAction.objects.filter(parent=obj,status__system_code__contains = "green").first()
            if rectified_flag:
                return mark_safe(
                    '<i class="fa fa-flag" style="color:{parent_flag_color}; font-size:25px"></i> '
                    '<i class="fa fa-flag" style="color:{flag_color}; font-size:25px"></i>'.format(
                        parent_flag_color=obj.status.color,
                        flag_color=rectified_flag.status.color
                    )
                )
            else:
                return None
        else:
            return None
        
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

    def get_description(self, obj):
        if obj:
            if obj.is_seen:
                return mark_safe('<p>{obsn}</p>'.format(
                    obsn = str(obj.description),
                ))
            return mark_safe('<p class="font-weight-bold">{obsn}</p>'.format(
                obsn = str(obj.description),
            ))
        else:
            return ""
    get_description.admin_order_field  = 'description'  #Allows column order sorting
    get_description.short_description = 'Obsn'  #Renames column head
    
    
    def edit_flag(self, obj):
        return mark_safe("<a href={url} style='text-align:center;'><i class='fa fa-edit text-170'></i></a>".format(
                url = reverse('admin:dashboard_rectifiedflag_change', args=[obj.pk])
            ))
    
    edit_flag.short_description = 'Edit Flag'

    def get_obsn(self, obj):
        return mark_safe('<a onclick="DashboardApi.obsnModal(\'{desc}\')" href="javascript:void(0);" class="btn btn-bold btn-outline-primary btn-h-primary fs--outline border-0 btn-a-primary radius-0 px-35 mb-1" data-toggle="tooltip" data-original-title="Flag Detail">Show Obsn</a>'.format(
                desc = str(obj.description),
        ))
    get_obsn.admin_order_field  = 'Description'  #Allows column order sorting
    get_obsn.short_description = ''  #Renames column head
   
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
        request, extra_context=extra_context)
        
        try:
            task_action_manager = TaskActionManager(TaskAction,request)
            qs = task_action_manager.get_pending_flags()
            rectified_qs = task_action_manager.get_rectified_flags()

        except (AttributeError, KeyError):
            return response
        
        self.request = request
        extra_context = extra_context or {}
       
        # Regions from Project Qs
        regions = rectified_qs.values_list('project__region', flat=True).distinct()
        regions_qs = Region.objects.filter(id__in=regions)
        # Cities from Project Qs
        cities_qs = City.objects.filter(region__in = regions_qs)

        # Region Card Filter
        region_counts = []
        total = 0

        for region in regions_qs:
            common_filter = Q(project__region=region)
            if 'drf__created_on__gte' in request.GET and 'drf__created_on__lte' in request.GET:
                common_filter &= Q(created_on__date__gte=request.GET['drf__created_on__gte'], created_on__date__lte=request.GET['drf__created_on__lte'])
            count = rectified_qs.filter(common_filter).count()
            total += count

            data_dict = {
                "id": str(region.id),
                "region_name": region.name,
                "region_count": count
            }
            region_counts.append(data_dict)

        extra_context['region_counts'] = region_counts
        extra_context['region_counts_total'] = total
    
    
    
        # Station Card Filter
        cities_counts = []
        total = 0

        if 'project__region_id' in request.GET:
            project_cities = cities_qs.filter(region_id=request.GET['project__region_id'])
        elif 'project__city_id' in request.GET:
            project_cities = cities_qs.filter(id=request.GET['project__city_id'])

        for city in cities_qs:
            common_filter = Q(project__city=city)
            if 'drf__created_on__gte' in request.GET and 'drf__created_on__lte' in request.GET:
                common_filter &= Q(created_on__date__gte=request.GET['drf__created_on__gte'], created_on__date__lte=request.GET['drf__created_on__lte'])

            count = rectified_qs.filter(common_filter).count()
            total += count

            data_dict = {
                "id": str(city.id),
                "region_id": str(city.region.id),
                "city_name": city.name,
                "city_count": count
            }
            cities_counts.append(data_dict)

        extra_context['cities_counts'] = cities_counts
        extra_context['city_counts_total'] = total


        insp_flag_filtered_query_set = qs.filter(status__parent__system_code = "system_status_task_status_inspection")
        mat_flag_filtered_query_set = qs.filter(status__parent__system_code = "system_status_task_status_material")
     
        # extra_context['mat_flag_filtered_query_set'] = self.getFlagStats(mat_flag_filtered_query_set,"material")
        # extra_context['ins_flag_filtered_query_set'] = self.getFlagStats(insp_flag_filtered_query_set,"inspection")
        extra_context['inspection_flag_stats'] = task_action_manager.get_inspection_flags_stats()
        extra_context['material_flag_stats'] = task_action_manager.get_material_flags_stats()
        extra_context['selected_filters'] = self.selectedFilter(request)
        extra_context['total_projects'] = Project.objects.filter().count()

        # Aggregate the number of TaskAction entries per region
        region_counts = qs.values('project__region__name').annotate(count=Count('project__region__name')).order_by('project__region__name')
        # Format the data as required
        data = [
            {
                'name': region_data['project__region__name'],
                'y': region_data['count']  # This is a count; adjust if you need a percentage or another metric
            }
            for region_data in region_counts
        ]

        extra_context['zonewise_graph_data'] = data

        # Timesince Select Filter
        extra_context['time_since_filter_form'] = TimeSinceFilterForm() 
        extra_context['flag_filter_form'] = FlagFilterForm(request=request) 


        ####### Pie Chart for Inspection Flags #######
        dataset_flag_pie = list(qs.values('status__color',name = F('status__name')).annotate(y = Count('status')))
        dataset_flag_pie_color = list()
        for entry in dataset_flag_pie:
            dataset_flag_pie_color.append(entry['status__color'])
       
        ####### Pie Chart For RegionWise Inspection Distribution Of Projects #######
        region_data = list(qs.filter(status__parent__system_code = 'system_status_task_status_inspection').order_by('project__region__ordering').values(('project__region__name')).distinct().annotate(name = F('project__region__name'),y = Count('id')))
        extra_context['dataset_inspection'] = dataset_flag_pie
        extra_context['dataset_region1'] = region_data
        extra_context['dataset_color'] = dataset_flag_pie_color
   
        ####### Pie Chart For RegionWise Material Distribution Of Projects #######
        region_data = list(qs.filter(status__parent__system_code = 'system_status_task_status_material').order_by('project__region__ordering').values(('project__region__name')).distinct().annotate(name = F('project__region__name'),y = Count('id')))
        extra_context['dataset_inspection'] = dataset_flag_pie
        extra_context['dataset_region2'] = region_data
        extra_context['dataset_color'] = dataset_flag_pie_color

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
    

    # Selected Filter Helper  Function
    def selectedFilter(self,request):
        formatted_string = ""
        if 'flag_id' in request.GET:
            flag_id = request.GET.get('flag_id',None)
            task_status = TaskStatus.objects.filter(id = flag_id).first()
            formatted_string = formatted_string + str(task_status.parent.name) + "-" + str(task_status.name) +" /"
        
        if 'project__city_id' in request.GET:
            city_id = request.GET.get('project__city_id',None)
            city = City.objects.filter(id = city_id).first()
            formatted_string = formatted_string + str(city.region.name) + "-" + str(city.name) + "/"

        if 'project__region_id' in request.GET:
            region_id = request.GET.get('project__region_id',None)
            region = Region.objects.filter(id = region_id).first()
            formatted_string = formatted_string + str(region.name) + "/"
        
        if 'status__parent_id' in request.GET:
            status_parent_id = request.GET.get('status__parent_id',None)
            status_parent = SystemStatus.objects.filter(parent_id = status_parent_id).first()
            formatted_string = formatted_string + str(status_parent.parent.name) + "/"
        
        if 'status_id' in request.GET:
            status_id = request.GET.get('status_id',None)
            status = SystemStatus.objects.filter(id = status_id).first()
            formatted_string = formatted_string + str(status.name) + "/"
        
        if 'drf__created_on__gte' and 'drf__created_on__lte' in request.GET.keys():
            drf__created_on__gte = request.GET.get('drf__created_on__gte',None)
            drf__created_on__lte = request.GET.get('drf__created_on__lte',None)
            formatted_string = formatted_string + str(drf__created_on__gte) + "  To  " + str(drf__created_on__lte) + "/"
        
        if 'project__organization__id__exact' in request.GET:
            organization_id = request.GET.get('project__organization__id__exact',None)
            organization = Organization.objects.get(id=organization_id)
            formatted_string = formatted_string + str(organization.name) + "/"
      
        return formatted_string


    # # This will help you to disable delete functionaliyt
    def get_queryset(self, request):
        task_action_manager = TaskActionManager(TaskAction,request)
        qs = task_action_manager.get_rectified_flags()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs.order_by('-created_on')
        
    def has_delete_permission(self, request, obj=None):
        if 'dashboard.can_delete_flag' in request.user.get_group_permissions(): 
            return True
        else:
            return False
    

    def has_add_permission(self, request):
        return False

    # def has_change_permission(self, request, obj=None):
    #     if 'dashboard.change_rectifiedflag' in request.user.get_group_permissions():
    #         return True
    #     else:
    #         return False

    def has_view_permission(self, request, obj=None):
        if 'dashboard.view_rectifiedflag' in request.user.get_group_permissions() or request.user.is_superuser: 
            return True
        else:
            return False

admin.site.register(RectifiedFlag,RectifiedFlagAdmin)


