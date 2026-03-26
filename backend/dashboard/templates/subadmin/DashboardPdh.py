from django.contrib import admin
from core.models import SystemStatus,User
from dashboard.models import DashboardPdh
#from daterange_filter.filter import DateRangeFilter
from utils.IP import get_client_ip
# from dashboard.utils.generateReport import generate_project_report_pdf
# Extras Import
from django.contrib import admin
from core.submodels.SystemStatus import SystemStatus
from organization.models import City,Region
from project.models import TaskAction,TaskActionComment
from project.submodels.TaskStatus import TaskStatus
from utils.IP import get_client_ip 
from datetime import datetime
from django.db.models import Count
from datetime import datetime, timedelta
from dashboard.utils.filterUserBasedQs import weekly_obsns_datefilter,filtered_qs_rolebased,filtered_region_rolebased,filtered_city_rolebased
from django.contrib.admin import SimpleListFilter
#  Packages for date
import json
from django.db.models import Subquery,F
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, DateTimeField
from django.db.models.functions import Trunc




class FlagsFilter(SimpleListFilter):
    title = 'Flags' # or use _('country') for translated title
    parameter_name = 'flag_id'

    def lookups(self, request, model_admin):
        return [(c.id, c.name+ "("+c.parent.name+")") for c in TaskStatus.objects.all()]
    def queryset(self, request, queryset):
        if self.value():
            return queryset

class RegionFilter(SimpleListFilter):
    title = 'Region' # or use _('country') for translated title
    parameter_name = 'region_id'

    def lookups(self, request, model_admin):
        # statuses = set([c.status for c in model_admin.model.objects.order_by('status__system_code').distinct('status__system_code')])
        filtered_regions =  set([c.region for c in model_admin.model.objects.order_by('region__code').distinct('region__code')])
        return [(c.id, c.name) for c in filtered_regions]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(region_id__exact=self.value())



class DashboardPdhAdmin(admin.ModelAdmin):
    list_display_links = None
    change_list_template = 'dashboard_pdh.html'
    list_display = ('region','city','organization','code','name','consultant_name','created_on','created_by','updated_on','updated_by')
    list_filter = (FlagsFilter,RegionFilter,'contract_status')
    readonly_fields = ["region","city","type","created_on","updated_on","created_by","updated_by"]
    exclude = ("ip","created_by","updated_by")
    # actions = [generate_project_report_pdf,]
    date_hierarchy = 'created_on'

    #fields = ('name', 'image', 'description')

    fieldsets = (
        ('User & Groups Info', {
            'fields': (('users', 'groups'))
        }),
        ('Organization Info', {
            'fields': (('region','city','type'),('organization','thumbnail'))
        }),
        ('Project Info', {
            'fields': (('name','code'), ('consultant_name','contract_status','expenditure_total'), 'category', 'status','start_date', 'end_date', 'project_remarks')
        }),
    )
    # search_fields = ('name','code','contract_status', 'created_on', 'updated_on')
    ordering = ('name','code','contract_status', 'created_on', 'updated_on')

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request, extra_context=extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        self.request = request
        extra_context = extra_context or {}

        # Base Querysets
        project_cities = City.objects.filter(id__in = filtered_city_rolebased(request,qs))
        project_qs = qs
        tasks_action_qs = TaskAction.objects.filter(project_id__in=Subquery(project_qs.values('id')))

        if 'region_id' in request.GET.keys():
            region_id = request.GET.get('region_id',None)
            if region_id:
                project_qs = project_qs.filter(region_id = region_id)
                tasks_action_qs = tasks_action_qs.filter(project_id__in=Subquery(project_qs.values('id')))

        if 'city_id' in request.GET.keys():
            city_id = request.GET.get('city_id',None)
            if city_id:
                project_qs = project_qs.filter(city_id__in = Subquery(project_cities.filter(id = city_id).values('id')))
                tasks_action_qs = tasks_action_qs.filter(project_id__in=Subquery(project_qs.values('id')))
                # inspection_flags = inspection_flags.filter(id__in = Subquery(tasks_action_qs.values('status__parent_id')))

        if 'flag_id' in request.GET.keys():
            tasks_action_qs = tasks_action_qs.filter(status__id = request.GET['flag_id'])

        # Totals
        extra_context['total_projects'] = qs.count()
        extra_context['qs'] = qs
        

        """ PIE CHART FOR SITE INSPECTION FLAGS """
        dataset_inspection_flag_pie = list(tasks_action_qs.filter(status__parent__system_code = 'system_status_task_status_inspection').values('status__color',name = F('status__name')).annotate(y = Count('status')))
        dataset_inspection_flag_pie_color = list()
        for entry in dataset_inspection_flag_pie:
            dataset_inspection_flag_pie_color.append(entry['status__color'])

        extra_context['dataset_inspection_flag_pie'] = dataset_inspection_flag_pie
        extra_context['dataset_inspection_flag_pie_color'] = dataset_inspection_flag_pie_color
        
        """ PIE CHART FOR SITE MATERIAL FLAGS """
        dataset_material_flag_pie = list(tasks_action_qs.filter(status__parent__system_code = 'system_status_task_status_material').values('status__color',name = F('status__name')).annotate(y = Count('status')))
        dataset_material_flag_pie_color = list()
        for entry in dataset_material_flag_pie:
            dataset_material_flag_pie_color.append(entry['status__color'])
    
        extra_context['dataset_material_flag_pie'] = dataset_material_flag_pie
        extra_context['dataset_material_flag_pie_color'] = dataset_material_flag_pie_color
        
        ####### Pie Chart for Inspection Flags #######
        dataset_flag_pie = list(tasks_action_qs.values('status__color',name = F('status__name')).annotate(y = Count('status')))
        dataset_flag_pie_color = list()
        for entry in dataset_flag_pie:
            dataset_flag_pie_color.append(entry['status__color'])
        
        ####### Pie Chart For RegionWise Distribution Of Projects #######
        region_data = list(project_qs.order_by('region__ordering').values(('region__name')).distinct().annotate(name = F('region__name'),y = Count('id')))

        # print(region_data)
        
        extra_context['dataset_inspection'] = dataset_flag_pie
        extra_context['dataset_region'] = region_data
        extra_context['dataset_color'] = dataset_flag_pie_color

        #######  BAR CHART FOR MATERIAL AND INSPECTION FLAGS ###############
        
        date_list = list()
        bar_color = []
        list_with_dict = list()
        
        type_of_flags = list(TaskStatus.objects.filter(parent__system_code = 'system_status_task_status_inspection').values_list('name',flat=True))
        for type in type_of_flags:
            dict_flag = dict()
            dict_flag['name'] = str(type).strip()
            dict_flag['data'] = list()
            list_with_dict.append(dict_flag)         
     
        # print(list_with_dict)
        bar_color = list(TaskStatus.objects.filter(parent__system_code = 'system_status_task_status_inspection').values_list('color',flat=True))

        if hasattr(self, 'date_hierarchy'):
            period = self._get_chart_period(request)
            data = qs.annotate(
                x=Trunc(
                    self.date_hierarchy,
                    period,
                    output_field=DateTimeField()
                )
            ).values('x').order_by('x').distinct()#.annotate(y=Count('team_level')).order_by('y')
        
            for date in data:
                if period == 'hour':
                    date_list.append(date['x'].strftime("%I %p"))

                if period == 'day':
                    date_list.append(date['x'].strftime("%b %d"))
                    by_day_task_actions = tasks_action_qs.filter(project__created_on__date = date['x'].strftime('%Y-%m-%d'))
                    flag_qs = by_day_task_actions.values('status__name','status__color').annotate(data = Count('status'))
                    for entry in flag_qs:
                        for dictionary in list_with_dict:
                            if dictionary['name'] == entry['status__name']:
                                dictionary['data'].append(entry['data'])

                if period == 'week':
                    date_list.append(date['x'].strftime("%b %d,%Y"))
                    by_day_task_actions = tasks_action_qs.filter(project__created_on__month = date['x'].strftime('%m'))
                    flag_qs = by_day_task_actions.values('status__name','status__color').annotate(data = Count('status'))
                    for entry in flag_qs:
                        for dictionary in list_with_dict:
                            if dictionary['name'] == entry['status__name']:
                                dictionary['data'].append(entry['data'])
                
                if period == 'month':
                    if not date['x'].strftime("%Y") in date_list:
                        date_list.append(date['x'].strftime("%Y"))
                        by_day_task_actions = tasks_action_qs.filter(project__created_on__year = date['x'].strftime('%Y'))
                        flag_qs = by_day_task_actions.values('status__name','status__color').annotate(data = Count('status'))
                        for entry in flag_qs:
                            for dictionary in list_with_dict:
                                if dictionary['name'] == entry['status__name']:
                                    dictionary['data'].append(entry['data'])

                   
            extra_context['chart_data'] = json.dumps(
                date_list, cls=DjangoJSONEncoder)
        
            extra_context['series_flag_bar'] = json.dumps(
                list_with_dict, cls=DjangoJSONEncoder)
            
            extra_context['bar_color'] = json.dumps(
                bar_color, cls=DjangoJSONEncoder)
          
        ####### END BAR CHART FOR MATERIAL AND INSPECTION FLAGS ###############
        
        """ USER ACTIVITY LOGGED IN"""
        last_five_logged_in_users = User.objects.filter(last_login__isnull = False).order_by('last_login')[:5]
        extra_context['last_five_logged_in_users'] = last_five_logged_in_users
       
        """ USER ACTIVITY LOGGED OUT """
        last_five_logged_out_users = User.objects.filter(last_logout__isnull = False).order_by('last_logout')[:5]
        extra_context['last_five_logged_out_users'] = last_five_logged_out_users
       
        """ USER THAT INDULGE IN LAST FIVE COMMENTS """
        last_five_comments = TaskActionComment.objects.filter(latitude__isnull = False).order_by('task_action_id','-created_on').distinct('task_action_id')[:5]
        extra_context['last_five_comments'] = last_five_comments
        
        
        return super(DashboardPdhAdmin, self).changelist_view(request, extra_context=extra_context)

    def _get_chart_period(self, request):
        if self.date_hierarchy + '__day' in request.GET:
            return 'hour'
        if self.date_hierarchy + '__month' in request.GET:
            return 'day'
        if self.date_hierarchy + '__year' in request.GET:
            return 'week'
        return 'month'

    
    # This will help you to disable delete functionaliyt
    def get_queryset(self, request):
        qs = self.model._default_manager.get_queryset()
        return qs
        # try:
        #     qs = self.model._default_manager.get_queryset()
        #     # qs = qs.filter(region__in=request.user)
        #     project_ids_list = filtered_qs_rolebased(request,qs)
        #     qs = qs.filter(id__in = project_ids_list)
        #     if request.GET and 'e' not in request.GET.keys():
        #         self.request = request
        #         flag_id = request.GET.get('flag_id',None)
        #         """
        #         Returns a QuerySet of all model instances that can be edited by the
        #         admin site. This is used by changelist_view.
        #         """
        #         if flag_id:
        #             #qs = self.model._default_manager.get_queryset().filter(project_taskactions__status_id=flag_id).order_by('-created_on')
        #             uniq_project_ids = list(TaskAction.objects.filter(status_id = flag_id).values_list('project_id',flat=True).distinct())
        #             qs = qs.filter(id__in = uniq_project_ids)
        #         # TODO: this should be handled by some parameter to the ChangeList.
        #         ordering = self.get_ordering(request)
        #         if ordering:
        #             qs = qs.order_by(*ordering)
        #         return qs
        #     else:
        #         qs = qs
        #     return qs 
        # except:
        #     pass
    
    
    # Weekly Obsns Helper Functions
    def weekly_obsns(self,task_action_qs):
        task_action_qs = task_action_qs.filter(created_on__gte=datetime.now()-timedelta(days=7))
        if task_action_qs:
            return task_action_qs
        else:
            return TaskAction.objects.none()  
    
    # Selected Filter Helper  Function
    def selectedFilter(self):
        formatted_string = ""
        if 'flag_id' in self.request.GET:
            flag_id = self.request.GET.get('flag_id',None)
            task_status = TaskStatus.objects.filter(id = flag_id).first()
            formatted_string = formatted_string + str(task_status.parent.name) + "-" + str(task_status.name) +" /"
        
        if 'city_id' in self.request.GET:
            city_id = self.request.GET.get('city_id',None)
            city = City.objects.filter(id = city_id).first()
            formatted_string = formatted_string + str(city.region.name) + "-" + str(city.name) + "/"

        if 'region_id' in self.request.GET:
            region_id = self.request.GET.get('region_id',None)
            region = Region.objects.filter(id = region_id).first()
            formatted_string = formatted_string + str(region.name) + "/"
        
        if 'inspection_id' in self.request.GET:
            inspection_id = self.request.GET.get('inspection_id',None)
            inspection = SystemStatus.objects.filter(id = inspection_id).first()
            formatted_string = formatted_string + str(inspection.name) + "/"

        return formatted_string


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
            
        if db_field.name == "status":
            kwargs["queryset"] = SystemStatus.objects.filter(parent__system_code__in =['system_status_project_status'])               #kwargs['disabled'] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request):
        return False
        if request.user.is_superuser == 0:
            return False
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return True
        else:
            return False

    def has_view_permission(self, request, obj=None):
        if not request.user.is_superuser:
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
     
        if obj.region is None and obj.city is None:
            obj.region = obj.organization.region
            obj.city = obj.organization.city
        
        super().save_model(request, obj, form, change)

admin.site.register(DashboardPdh,DashboardPdhAdmin)
