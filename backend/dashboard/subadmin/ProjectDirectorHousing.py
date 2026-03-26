import calendar
import json
from re import T
from django.contrib import admin
from core.submodels.SystemStatus import SystemStatus
from dashboard.models import ProjectDirectorHousing
from organization.models import City,Region
from project.models import Task,TaskAction,TaskActionComment,TaskFile,TaskActionTimeLine
from project.submodels.TaskStatus import TaskStatus
from utils.IP import get_client_ip
from django.contrib.admin import SimpleListFilter
from django.db.models import Subquery,F,Q
from django.urls import re_path
from django.http import HttpResponse,JsonResponse
from dashboard.serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from core.models import User
from django.shortcuts import render
from datetime import datetime,timedelta
from django.template.response import TemplateResponse
from django.db.models import Count
from django.utils.safestring import mark_safe
from notifications.signals import notify
from dashboard.utils.filterUserBasedQs import weekly_obsns_datefilter,filtered_qs_rolebased,filtered_region_rolebased,filtered_city_rolebased
from daterange_filter.filter import DateRangeFilter
from core.models import SystemType,UserTypeHierarchy
from project.models import Project
from dashboard.utils.flag_management import TaskActionManager
from collections import defaultdict
from django.db.models.functions import ExtractYear
from django.db.models import Count, OuterRef, Subquery
from datetime import datetime, timedelta
from django.utils.timezone import now
from django import forms
from django.utils.translation import gettext_lazy as _
from django.urls import path
from datetime import datetime
from collections import defaultdict
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse


class CityFilter(SimpleListFilter):
    title = 'City' # or use _('country') for translated title
    parameter_name = 'project__city_id'

    def lookups(self, request, model_admin):
        # statuses = set([c.status for c in model_admin.model.objects.order_by('status__system_code').distinct('status__system_code')])
        cities =  set([c.project.city for c in model_admin.model.objects.order_by('project__city__code').distinct('project__city__code')])
        return [(c.id, c.name) for c in cities]
    def queryset(self, request, queryset):

        if self.value():
            return queryset.filter(project__city_id__exact=self.value())

class RegionFilter(SimpleListFilter):
    title = 'Region' # or use _('country') for translated title
    parameter_name = 'project__region_id'

    def lookups(self, request, model_admin):
        # statuses = set([c.status for c in model_admin.model.objects.order_by('status__system_code').distinct('status__system_code')])
        filtered_regions =  set([c.project.region for c in model_admin.model.objects.order_by('project__region__code').distinct('project__region__code')])
        return [(c.id, c.name) for c in filtered_regions]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(project__region_id__exact=self.value())


class OrganizationFilter(SimpleListFilter):
    title = 'Organization' # or use _('country') for translated title
    parameter_name = 'project__organization_id'

    def lookups(self, request, model_admin):
        # statuses = set([c.status for c in model_admin.model.objects.order_by('status__system_code').distinct('status__system_code')])
        filtered_organizations =  set([c.project.organization for c in model_admin.model.objects.filter(project__organization__status="active").order_by('project__organization__code').distinct('project__organization__code')])
        return [(c.id, c.name) for c in filtered_organizations]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(project__organization_id__exact=self.value())


class InspectionFilter(SimpleListFilter):
    title = 'Inspection' # or use _('country') for translated title
    parameter_name = 'inspection_id'

    def lookups(self, request, model_admin):
        return [(c.status.parent.id, c.status.parent.name) for c in TaskAction.objects.distinct('status__parent')]
    def queryset(self, request, queryset):

        if self.value():
            return queryset.filter(project_taskactions__status__parent_id=self.value())

class FlagsFilter(SimpleListFilter):
    title = 'Flags' # or use _('country') for translated title
    parameter_name = 'flag_id'

    def lookups(self, request, model_admin):
        return [(c.id, c.name+ "("+c.parent.name+")") for c in TaskStatus.objects.all()]
    
    def queryset(self, request, queryset):
        if self.value():
            project_ids = TaskAction.objects.filter(status_id = self.value(),end_time__isnull=True).order_by('-created_on').values_list('project_id',flat=True)
            return queryset.filter(id__in=project_ids)

class YearFilter(admin.SimpleListFilter):
    title = _('Year')
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        current_year = datetime.now().year
        return [(str(year), str(year)) for year in range(current_year, current_year - 5, -1)]

    def queryset(self, request, queryset):
        # value = self.value()
        # if value:
        #     return queryset.filter(created_on__year=value)
        return queryset


class ProjectDirectorHousingAdmin(admin.ModelAdmin):
    # change_list_template = 'admin/dashboard/change_list.html'
    #change_form_template = 'admin/dashboard/change_form.html'
    
    change_list_template = 'change_list.html'
    # change_form_template = 'change_form.html'
    list_display_links = None
    # list_display = ('reference_number','name', 'get_flags','progress_actual','consultant_name')
    readonly_fields = ('get_flags',)
    show_full_result_count = False
    list_filter = (('created_on',DateRangeFilter),YearFilter,OrganizationFilter)
    list_per_page = 5


    # search_fields = ('code','name', 'consultant_name','contractor_name','status__name', 'start_date', 'end_date')
    # ordering = ('name','code','status', 'created_on', 'updated_on')

    def get_flags(self, obj,inspection_id = None,flag_id = None):
        flag_id = self.request.GET.get('flag_id', None)
        if flag_id is not None:
            if obj.project_taskaction_related is not None:
                if flag_id:
                    filtered_qs = obj.project_taskaction_related.filter(status_id=flag_id,end_time__isnull = True)
                    if filtered_qs.first():
                        return mark_safe('<a onclick="getTaskActions({ca_id},{flag_id})" href="javascript:void(0);" class="insp1 btn bgc-white btn-light-secondary mx-0" data-toggle="tooltip" data-original-title="Flag Detail">\
                        {flag_count} <i class="fa fa-flag" style="color:{flag_color}"></i></a>'.format(
                            ca_id = obj.id,
                            flag_id = flag_id,
                            flag_color = filtered_qs.first().status.color, 
                            flag_count = filtered_qs.filter(status_id=flag_id,end_time__isnull = True).count()
                        ))
                else:
                    return str(obj.project_taskaction_related.count())
            else:
                return 0

        else:
            if obj.project_taskaction_related and obj.project_taskaction_related is not None:
                return obj.project_taskaction_related.all().count()

    get_flags.admin_order_field  = 'project_taskactions'  #Allows column order sorting
    get_flags.short_description = 'Flags'  #Renames column head

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
        regions = qs.values_list('project__region', flat=True).distinct()
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
            count = qs.filter(common_filter).count()
            total += count

            data_dict = {
                "id": str(region.id),
                "region_name": region.name,
                "region_count": count
            }
            region_counts.append(data_dict)
            # Sort the regions in predefined order
        region_order = ["NORTH", "CENTER", "SOUTH"]
        region_counts.sort(key=lambda x: region_order.index(x["region_name"]) if x["region_name"] in region_order else float('inf'))

        extra_context['region_counts'] = region_counts


        # extra_context['region_counts'] = region_counts
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

            count = qs.filter(common_filter).count()
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
        extra_context['selected_filters'] = self.selectedFilter()

        # Material Flag Card Filter
        material_flags_counts = []
        material_flags_counts_raised = 0
        material_flags_counts_cleared = 0
        material_flags_counts_balance = 0

        for region in regions_qs:
            for mat_flag in SystemStatus.objects.filter(system_code="system_status_task_status_material").first().get_descendants(include_self=False).exclude(system_code="system_status_task_status_material_green"):
                common_filter = Q(project__region=region, status=mat_flag)
                material_qs = qs.filter(common_filter)
                material_pending_qs = material_qs
                material_cleared_qs = rectified_qs.filter(common_filter)

                if material_pending_qs.exists() and material_cleared_qs.exists():
                    material_raised_qs = material_pending_qs.union(material_cleared_qs)
                else:
                    material_raised_qs = material_pending_qs or material_cleared_qs

                material_flags_counts_raised += material_raised_qs.count()
                material_flags_counts_cleared += material_cleared_qs.count()
                material_flags_counts_balance += material_pending_qs.count()

                data_dict = {
                    "id": str(mat_flag.id),
                    "flag_color": mat_flag.color,
                    "raised_count": material_raised_qs.count(),
                    "cleared_count": material_cleared_qs.count(),
                    "pending_count": material_pending_qs.count(),
                    "region_id": str(region.id)
                }

                if 'project__city_id' in request.GET:
                    data_dict['url'] = "/dashboard/taskactionlist/?status_id={flag_id}&project__city_id={city_id}".format(
                        flag_id=mat_flag.id, city_id=str(request.GET['project__city_id']))
                elif 'project__region_id' in request.GET:
                    data_dict['url'] = "/dashboard/taskactionlist/?status_id={flag_id}&project__region_id={region_id}".format(
                        flag_id=mat_flag.id, region_id=str(region.id))
                else:
                    data_dict['url'] = "/dashboard/taskactionlist/?status_id={flag_id}".format(flag_id=mat_flag.id)

                material_flags_counts.append(data_dict)
        
        extra_context['mat_flag_counts'] = list(material_flags_counts)
        extra_context['material_flags_counts_raised'] = material_flags_counts_raised
        extra_context['material_flags_counts_cleared'] = material_flags_counts_cleared
        extra_context['material_flags_counts_balance'] = material_flags_counts_balance
        
        # Inspection Flag Card Filter
        inspection_flags_counts = []
        inspection_flags_counts_raised = 0
        inspection_flags_counts_cleared = 0
        inspection_flags_counts_balance = 0
        for region in regions_qs:
            for ins_flag in SystemStatus.objects.filter(system_code="system_status_task_status_inspection").first().get_descendants(include_self=False).exclude(system_code="system_status_task_status_inspection_green"):
                common_filter = Q(project__region=region, status=ins_flag)
                inspection_qs = qs.filter(common_filter)
                inspection_pending_qs = inspection_qs
                inspection_cleared_qs = rectified_qs.filter(common_filter)

                if inspection_pending_qs.exists() and inspection_cleared_qs.exists():
                    inspection_raised_qs = inspection_pending_qs.union(inspection_cleared_qs)
                else:
                    inspection_raised_qs = inspection_pending_qs or inspection_cleared_qs

                inspection_flags_counts_raised += inspection_raised_qs.count()
                inspection_flags_counts_cleared += inspection_cleared_qs.count()
                inspection_flags_counts_balance += inspection_pending_qs.count()

                data_dict = {
                    "id": str(ins_flag.id),
                    "flag_color": ins_flag.color,
                    "raised_count": inspection_raised_qs.count(),
                    "cleared_count": inspection_cleared_qs.count(),
                    "pending_count": inspection_pending_qs.count(),
                    "region_id": str(region.id)
                }

                if 'project__city_id' in request.GET:
                    data_dict['url'] = "/taskactionlist/?status_id={flag_id}&project__city_id={city_id}".format(
                        flag_id=ins_flag.id, city_id=str(request.GET['project__city_id']))
                elif 'project__region_id' in request.GET:
                    data_dict['url'] = "/taskactionlist/?status_id={flag_id}&project__region_id={region_id}".format(
                        flag_id=ins_flag.id, region_id=str(region.id))
                else:
                    data_dict['url'] = "/taskactionlist/?status_id={flag_id}".format(flag_id=ins_flag.id)

                inspection_flags_counts.append(data_dict)
        extra_context['ins_flag_counts'] = list(inspection_flags_counts)
        extra_context['inspection_flags_counts_raised'] = inspection_flags_counts_raised
        extra_context['inspection_flags_counts_cleared'] = inspection_flags_counts_cleared
        extra_context['inspection_flags_counts_balance'] = inspection_flags_counts_balance

       
        # Month Wise Flag Stats with percentage
        # Get the current year
        # Current date
        now = datetime.now()
        # Calculate the first day of the current month
        first_day_current_month = now.replace(day=1)

        # List to hold the last five months
        last_five_months = [(first_day_current_month - timedelta(days=30 * i)).month for i in range(5)]

        # Sort the months in the correct order
        last_five_months.sort(key=lambda x: x)

      
        return super(ProjectDirectorHousingAdmin, self).changelist_view(request, extra_context=extra_context)
    

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('ajax-graph/inspection-flag-pie/', self.admin_site.admin_view(self.month_year_wise_stats_view), name='inspection_flag_pie'),
            path('ajax-graph/region-wise-distribution/', self.admin_site.admin_view(self.region_wise_distribution_view), name='region_wise_distribution'),
            path('ajax-graph/zonal-flag-stats/', self.admin_site.admin_view(self.zonal_flag_stats), name='zonal-flag-stats'),
            re_path(r'^task_action_flag_detail/$', self.get_task_action_flag_detail,name='task_action_flag_detail'),
            re_path(r'^task_action_first_attachment/$', self.task_action_first_attachment,name='task_action_flag_detail'),
            re_path(r'^task_action_chat_detail/$', self.get_task_action_chat_detail,name='task_action_chat_detail'),
            re_path(r'^organization_hierarchy/$', self.getOrganizationHierarchyUsers, name='organization_hierarchy_users'),
            re_path(r'^pdh_task_detail/(?P<id>\d+)/$', self.getPdhTaskDetail, name='pdh_task_detail'),
            re_path(r'^comment_reply/$', self.getCommentReply, name='get_comment_reply'),
            re_path(r'^bell_notifications/$', self.getBellNotifications, name='get_bell_notifications'),
            re_path(r'^get_users/$', self.getUsers, name='get_users'),
            re_path(r'^get_task_actions/$', self.getTaskActions, name='get_task_actions'),
            re_path(r'^get_notification_task_action/$', self.getNotificationTaskAction, name='get_notification_task_action'),
            re_path(r'^get_task_action_attachments/$', self.getTaskActionAttachments, name='get_task_action_attachments'),
        ]
        return custom_urls + urls

    def inspection_flag_pie_view(self, request):
        task_action_manager = TaskActionManager(TaskAction,request)
        qs = task_action_manager.get_qs()
        # Pie Chart for Inspection Flags
        dataset_flag_pie = list(
            qs.values('status__color', name=F('status__name')).annotate(y=Count('status'))
        )
        dataset_flag_pie_color = [entry['status__color'] for entry in dataset_flag_pie]
        
        # Pie Chart For RegionWise Distribution Of Projects
        region_data = list(
            qs.order_by('project__region__ordering')
              .values('project__region__name')
              .distinct()
              .annotate(name=F('project__region__name'), y=Count('id'))
        )
        
        # Prepare the response data
        response_data = {
            'dataset_inspection': dataset_flag_pie,
            'dataset_region': region_data,
            'dataset_color': dataset_flag_pie_color,
        }

        return JsonResponse(response_data)

  





   # Zone Wise Report
    def region_wise_distribution_view(self, request):
        task_action_manager = TaskActionManager(TaskAction, request)
        
        # Use select_related for better performance
       # qs = task_action_manager.get_qs().filter(created_on__year=2025).select_related('status', 'project')
        qs = task_action_manager.get_qs().select_related('status', 'project')

        
        status_counts_regionwise = defaultdict(lambda: defaultdict(int))
        status_colors_dict = {}

        # Process the queryset in one go
        for item in qs.filter(status__isnull=False):
            status_name = item.status.name
            region_name = item.project.region.name

            if 'green' not in item.status.system_code:
                status_counts_regionwise[region_name]['pending'] += 1
                status_counts_regionwise[region_name]['raised'] += 1
            else:
                status_counts_regionwise[region_name]['raised'] += 1
                status_counts_regionwise[region_name]['cleared'] += 1
            
            # Store status colors
            status_colors_dict.setdefault(status_name, item.status.color)

        # Debug: Print regions before sorting
        print("Before Sorting:", list(status_counts_regionwise.keys()))

        # Enforce specific region order
        region_order = ["NORTH", "CENTER", "SOUTH"]
        distinct_regions = sorted(
            status_counts_regionwise.keys(),
            key=lambda region: region_order.index(region) if region in region_order else float('inf')
        )

        with open('/tmp/debug_log.txt', 'w') as debug_file:
         json.dump(distinct_regions, debug_file, indent=4)

      

        distinct_statuses = ['raised', 'cleared', 'pending']
        series_data = [
        {
        'name': status.capitalize(),
        'data': [status_counts_regionwise.get(region, {}).get(status, 0) for region in distinct_regions]
        }
         for status in distinct_statuses
         ]
        # series_data = [
        #     {
        #         'name': status.capitalize(),
        #         'data': [status_counts_regionwise[region].get(status, 0) for region in distinct_regions]
        #     }
        #     for status in distinct_statuses
        # ]

        # Define colors for each status
        colors = ['#5c5ced', '#32CD32', '#FF6347']

        # Prepare response data
        response_data = {
            'region_wise_flag_percentage_data_series_data': series_data,
            'region_wise_flag_percentage_data_colors': colors,
            'region_wise_flag_percentage_data_regions': distinct_regions  # Check if order is correct
        }

        # Debug: Print final response data
        print("Final Response:", response_data)

        return JsonResponse(response_data)



   

     # Month Wise Report
    def month_year_wise_stats_view(self, request):
        now = datetime.now()
        first_day_current_month = now.replace(day=1)

        # Get the last five months accurately with correct days in each month
        last_five_months = []
        for i in range(5):
            month_date = first_day_current_month - relativedelta(months=i)
            last_day = calendar.monthrange(month_date.year, month_date.month)[1]  # Get last day of month
            last_five_months.append((month_date.replace(day=1), month_date.replace(day=last_day)))  # Store (first_day, last_day)

        last_five_months.reverse()  # Ensure chronological order (earliest first)

        # Initialize a defaultdict to hold status counts
        status_counts_monthwise = defaultdict(lambda: defaultdict(int))
        status_colors_dict = {}

        # Determine the year to filter by
        current_year = now.year
        if 'drf__created_on__gte' in request.GET and 'drf__created_on__lte' in request.GET:
            drf__created_on__lte = request.GET.get('drf__created_on__lte', None)
            current_year = datetime.strptime(drf__created_on__lte, "%Y-%m-%d").year

        # Assuming `qs` is the queryset you want to analyze
        task_action_manager = TaskActionManager(TaskAction, request)
        qs = task_action_manager.get_pending_flags()

        for item in qs:
            status_name = item.status.name
            created_month = item.created_on.strftime('%b %Y')  # Store month & year as key
            status_counts_monthwise[created_month][status_name] += 1

            # Extract status colors
            status_color = item.status.color
            status_colors_dict[status_name] = status_color

        # Filter out months with empty data dictionaries
        status_counts_monthwise = {month: status_counts for month, status_counts in status_counts_monthwise.items() if status_counts}

        # Initialize a list to hold the series data
        series_data = []
        distinct_statuses = set(status for status_counts in status_counts_monthwise.values() for status in status_counts.keys())

        for status in distinct_statuses:
            data = []
            for first_day, last_day in last_five_months:
                month_label = first_day.strftime('%b %Y')  # Convert month object to string
                count = status_counts_monthwise.get(month_label, {}).get(status, 0)
                data.append(count)
            series_data.append({'name': status, 'data': data})

        # Extract colors for each status
        colors = [status_colors_dict[status] for status in distinct_statuses]

        # Prepare the response data
        response_data = {
            'month_wise_data_series': series_data,
            'month_labels': [first_day.strftime('%b %Y') for first_day, _ in last_five_months],  # Correct month-year labels
            'month_wise_colors': colors,
        }

        return JsonResponse(response_data)
      # Flag Stats Per Zone
    def zonal_flag_stats(self, request):
        task_action_manager = TaskActionManager(TaskAction, request)
        qs = task_action_manager.get_pending_flags()

        # Subquery to count TaskActions per region
        task_action_count_subquery = qs.filter(
         project__region=OuterRef('pk'),
         project__region__status='active'
        ).values('project__region').annotate(count=Count('id')).values('count')

        # Main query to get active regions with TaskAction counts
        region_task_counts = Region.objects.filter(status='active').annotate(
        task_action_count=Subquery(task_action_count_subquery)
        ).values('name', 'task_action_count')

        # Predefined order for sorting
        region_order = ["CENTER", "NORTH", "SOUTH"]

        # Format and sort the data as required
        zonal_stats_formatted_data = sorted(
         [
            {
                'name': region['name'],
                'y': region['task_action_count'] if region['task_action_count'] is not None else 0
            }
            for region in region_task_counts
         ],
        key=lambda region: region_order.index(region['name']) if region['name'] in region_order else float('inf')
        )

        # Return the formatted data as JSON
        return JsonResponse(zonal_stats_formatted_data, safe=False)


    
  
   
    



    @csrf_exempt
    def getOrganizationHierarchyUsers(self,request):
        if request.method == 'GET':
            data = {}
            hierarchy_obj = UserTypeHierarchy.objects.filter(user_type=request.user.type,status="active").first()
            if hierarchy_obj:
                group_user_types = hierarchy_obj.group_user_types.all()
                users = User.objects.filter(type_id__in = Subquery(group_user_types.values('id')))
                users = users.annotate(type_ordering=F('type__tree_id'), type_lft=F('type__lft'))
                data['users'] = users.order_by('type__tree_id', 'type__lft')
            return TemplateResponse(request, 'partials/tag_modal_box_body.html', data)

    @csrf_exempt
    def task_action_first_attachment(self,request):
        if request.method == 'POST':
            id = request.POST.get("id",None)
            data = {}
            task_action = None
            task_action_obj = TaskAction.objects.filter(id = id).first()
          
            
            task_action_comment = TaskActionComment.objects.filter(task_action_id = id,reply=False).first()
            if task_action_comment:
                task_action_files = TaskFile.objects.filter(task_action_comment_id=task_action_comment.id)
                data = {'task_action_comment': task_action_comment,'task_action_files':task_action_files,'task_action':task_action}
            return TemplateResponse(request, 'partials/obsns_modal_box_body.html', data)
       
    @csrf_exempt
    def get_task_action_flag_detail(self,request):
        if request.method == 'POST':
            id = request.POST.get("id",None)
            task_action_comment = TaskActionComment.objects.filter(id = id).first()
            task_action_files = TaskFile.objects.filter(task_action_comment_id = id)
            data = {'task_action_comment': task_action_comment,'task_action_files':task_action_files}
            return TemplateResponse(request, 'partials/obsns_modal_box_body.html', data)
       
    @csrf_exempt
    def get_task_action_chat_detail(self,request):
        if request.method == 'POST':
            task_action_id = request.POST.get("id", None)
            task_action = TaskAction.objects.filter(id=task_action_id).first()
            if task_action:
                task_action_comments = TaskActionComment.objects.filter(Q(tag_to=request.user) | Q(tag_to__isnull=True)| Q(created_by=request.user),task_action_id=task_action_id).order_by('created_on')
                #task_action_files = TaskFile.objects.filter(task_action_id=task_action_id)
                data = {}
                data['task_id'] = task_action.task.id
                data['task_action'] = task_action
                data['task_action_comments'] = task_action_comments
                return TemplateResponse(request, 'partials/chat_box_body.html', data)
            return TemplateResponse(request, 'partials/chat_box_body.html')

    @csrf_exempt
    def getPdhTaskDetail(self,request,id):
        if request.method == 'POST':
            users = User.objects.all()
            data = UserSerializer(users, many=True).data
            if data:
                data = {'status': 1, 'data': {'users':data}}
                return JsonResponse(data)
            else:
                data = {'status': 0, 'data': {'msg': 'Order Not Founded'}}
                return JsonResponse(data)

        if request.method == 'GET':
            if request.user.type.code == "system_type_user_region":
                if id is not None:
                    task = Task.objects.filter(id = id).first()
                    if task is not None:
                        data = {}
                        data['task'] = task
                        return render(request, 'admin/dashboard/pdh_task_detail.html',data)
                    else:
                        return HttpResponse("Sorry! Data Not Founded")
                return HttpResponse("Sorry! Data Not Founded1")
            return HttpResponse("Sorry! Your Role not Allowed")
        return HttpResponse("Sorry! Method not Allowed")
    
    @csrf_exempt
    def getCommentReply(self,request):
        if request.method == 'POST':
            base_url = request.scheme + '://' + request.get_host() + '/'
            user_id = request.POST.get('tagged_user',None)
            comment = request.POST.get('comment_textbox',None)
            reply_id = request.POST.get('reply_id',None)
            task_action_id = request.POST.get('task_action_id',None)
            attachments = request.FILES.get('chat_attachment',None)
            if comment:
                parent = None
                task_action =  TaskAction.objects.filter(id=task_action_id).first()
                if reply_id:
                    parent = TaskActionComment.objects.get(id = reply_id)
                task_action_comment = TaskActionComment()
                if user_id:
                    task_action_comment.tag_to_id = user_id
                    task_action_comment.tag_from_id = request.user.id
                    task_action_comment.tag_time = datetime.now()
                if request.user:
                    task_action_comment.created_by_id = request.user.id
                task_action_comment.ip = get_client_ip(request)
                if parent:
                    task_action_comment.parent = parent
                
                task_action_comment.reply = True
                task_action_comment.project = task_action.project
                task_action_comment.task = task_action.task
                task_action_comment.task_action = task_action
                task_action_comment.type = task_action.type

                # task_action_comment.description = self.get_quill(comment)
                task_action_comment.description = str(comment)
                task_action_comment.status = task_action.status
                task_action_comment.save()
        
        
                if user_id:
                    page_number = request.GET.get('p')
                    sender = User.objects.get(id=request.user.id)
                    receiver = User.objects.get(id=user_id)
                    if page_number:
                        target_url = base_url+'dashboard/taskactionlist/?p='+page_number
                    else:
                        target_url = base_url+'dashboard/taskactionlist/'
                    
                    result = notify.send(sender, recipient=receiver,action_object= task_action, verb='Flag Tagged', description=comment)
                    if result[0]:
                        _,notification = result[0]
                        notify_obj = notification[0]
                        notify_obj.target_url = target_url
                        notify_obj.save()

             
            if attachments and task_action_comment:
                task_file = TaskFile()
                if user_id:
                    task_file.created_by_id = request.user.id
                task_file.ip = get_client_ip(request)
                task_file.project = task_action_comment.project
                task_file.task = task_action_comment.task_action.task
                task_file.task_action = task_action_comment.task_action
                task_file.task_action_comment = task_action_comment
                task_file.organization = task_action_comment.project.organization
                task_file.type = task_action_comment.type
                task_file.status = task_action_comment.status
                task_file.progress_planned = task_action_comment.progress_planned
                task_file.progress_actual = task_action_comment.progress_planned
                task_file.duration = task_action_comment.duration
                task_file.latitude = task_action_comment.latitude
                task_file.longitude = task_action_comment.longitude
                task_file.precision = task_action_comment.precision
                task_file.filename = attachments.name
                task_file.attachment = attachments
                task_file.save()

                data = {'status': 1, 'data': {'msg': 'Created Successfully'},'id':str(task_action_id)}
                return JsonResponse(data)
            else:
                data = {'status': 1, 'data': {'msg': 'Created Successfully'},'id':str(task_action_id)}
                return JsonResponse(data)
        else:
            data = {'status': 0, 'data': {'msg': 'Sorry! Method not Allowed'}}
            return JsonResponse(data)                
            #return HttpResponse("Sorry! Method not Allowed")

    @csrf_exempt
    def getUsers(self,request):
        type_organization = SystemType.objects.filter(system_code = request.user.type.system_code).first().get_descendants(include_self=False)
        parent_type_organization = SystemType.objects.filter(system_code = request.user.type.system_code).first().parent
        users = User.objects.filter(type_id__in = Subquery(type_organization.values('id'))).union(User.objects.filter(type_id = parent_type_organization.id))
        data = UserSerializer(users, many=True).data
        if data:
            data = {'status': 1, 'data': {'users':data}}
            return JsonResponse(data)
        else:
            data = {'status': 1, 'data': {'users':data}}
            return JsonResponse(data)
    
    @csrf_exempt
    def getTaskActions(self,request):
        if request.method == 'POST':
            project_id = request.POST.get("project_id",None)
            status_id = request.POST.get("status_id",None)
            task_action_qs = TaskAction.objects.filter(project_id = project_id,status_id=status_id,end_time__isnull=True).order_by("-created_on")

        return TemplateResponse(request,'helper_template/pdh_task_action.html',{'task_action_qs': task_action_qs})
    
    @csrf_exempt
    def getNotificationTaskAction(self,request):
        if request.method == 'POST':
            comment_id = request.POST.get("comment_id",None)
            task_action_obj = TaskActionComment.objects.filter(id = comment_id).first()
            task_action_obj.tag_seen = True
            if task_action_obj.is_acknowledged == False:
                task_action_obj.tag_seen = True
            task_action_obj.save()
            task_action_qs = TaskAction.objects.filter(id = task_action_obj.task_action.id)
        return TemplateResponse(request,'helper_template/pdh_task_action.html',{'task_action_qs': task_action_qs})
    
    @csrf_exempt
    def getTaskActionAttachments(self,request):
        if request.method == 'POST':
            task_action_id = request.POST.get("task_action_id",None)
            files = TaskFile.objects.filter(task_action_id = task_action_id)
            return TemplateResponse(request,'helper_template/flag_attachments_partial.html',{'attachments': files})

    @csrf_exempt
    def getBellNotifications(self,request):
        task_action_comment = (TaskActionComment.objects.filter(tag_to__isnull = False,tag_to_id = request.user.id) | TaskActionComment.objects.filter(tag_to__isnull = True, tag_from__isnull=True, is_acknowledged = False)).order_by("-created_on")[:6]
        # Updating Notification As Read
        request.user.notifications.mark_all_as_read()
        # task_action_comment_ct = ContentType.objects.get(app_label='project', model='taskactioncomment')
        # Notification.objects.filter(action_object_content_type = task_action_comment_ct,action_object_object_id__in = Subquery(task_action_comment.values("id"))).update(unread = False)
        return TemplateResponse(request,'helper_template/bell_messages.html',{'comments': task_action_comment,'count':task_action_comment.count()})



    def get_queryset(self, request):
        task_action_manager = TaskActionManager(TaskAction,request)
        qs = task_action_manager.get_pending_flags()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs.order_by('-created_on')

    # Selected Filter Helper  Function
    def selectedFilter(self):
        formatted_string = ""
        if 'flag_id' in self.request.GET:
            flag_id = self.request.GET.get('flag_id',None)
            task_status = TaskStatus.objects.filter(id = flag_id).first()
            formatted_string = formatted_string + str(task_status.parent.name) + " > " + str(task_status.name) +" > "
        
        if 'project__region_id' in self.request.GET:
            region_id = self.request.GET.get('project__region_id',None)
            region = Region.objects.filter(id = region_id).first()
            formatted_string = formatted_string + str(region.name) + " > "
        
        if 'project__city_id' in self.request.GET: 
            city_id = self.request.GET.get('project__city_id',None)
            city = City.objects.filter(id = city_id).first()
            formatted_string = formatted_string + str(city.name) + " > " 

        if 'inspection_id' in self.request.GET:
            inspection_id = self.request.GET.get('inspection_id',None)
            inspection = SystemStatus.objects.filter(id = inspection_id).first()
            formatted_string = formatted_string + str(inspection.name) + " > "
        
        if 'drf__created_on__gte' and 'drf__created_on__lte' in self.request.GET.keys():
            drf__created_on__gte = self.request.GET.get('drf__created_on__gte',None)
            drf__created_on__lte = self.request.GET.get('drf__created_on__lte',None)
            formatted_string = formatted_string + str(drf__created_on__gte) + "  To  " + str(drf__created_on__lte) + " > "

        return formatted_string

    def has_delete_permission(self, request, obj=None):
        return False
    
   

    def save_model(self, request, obj, form, change):
      
        obj.ip = get_client_ip(request)
        super().save_model(request, obj, form, change)

admin.site.register(ProjectDirectorHousing, ProjectDirectorHousingAdmin)