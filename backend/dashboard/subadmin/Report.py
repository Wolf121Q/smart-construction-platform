from django.contrib import admin
from core.submodels.SystemStatus import SystemStatus
from organization.models import City,Region
from project.models import TaskAction,Project,TaskStatus
from utils.IP import get_client_ip
from django.contrib.admin import SimpleListFilter
from django.db.models import Subquery,Sum,F
from django.urls import reverse
from django.db.models import Count
from dashboard.utils.filterUserBasedQs import weekly_obsns_datefilter,filtered_qs_rolebased
from daterange_filter.filter import DateRangeFilter
from django.utils.html import format_html
from collections import Counter
from dashboard.models import Report
from dashboard.utils.generateReport import generate_project_report_pdf


class CityFilter(SimpleListFilter):
    title = 'City' # or use _('country') for translated title
    parameter_name = 'city_id'

    def lookups(self, request, model_admin):
        # statuses = set([c.status for c in model_admin.model.objects.order_by('status__system_code').distinct('status__system_code')])
        cities =  set([c.city for c in model_admin.model.objects.order_by('city__code').distinct('city__code')])
        return [(c.id, c.name) for c in cities]
    def queryset(self, request, queryset):

        if self.value():
            return queryset.filter(city_id__exact=self.value())

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

class ReportAdmin(admin.ModelAdmin):
    list_display_links = None
    list_per_page = 10
    list_max_show_all = 100000000000
    change_list_template = 'report_change_list.html'
    list_display = ('project_reference_number','name', 'get_flags','get_project_station','get_project_contractor','task_progress','progress_difference','get_created_on','get_updated_on')
    list_filter = ('contract_status',('created_on', DateRangeFilter),CityFilter,RegionFilter,'organization')
    readonly_fields = ["region","city","type","created_on","updated_on","created_by","updated_by"]
    search_fields = ['reference_number','name','contractor','created_on','created_by','updated_on','updated_by']
    exclude = ("ip","created_by","updated_by")
    actions = [generate_project_report_pdf,]
    date_hierarchy = 'created_on'
    ordering = ('-updated_on','-created_on')

    def get_project_name(self, obj):
        return obj.name
    get_project_name.admin_order_field  = 'name'  #Allows column order sorting
    get_project_name.short_description = 'Type Of Work'  #Renames column head

    def get_flags(self, obj,inspection_id = None,flag_id = None):
        task_actions = obj.project_taskaction_related.all()
        if task_actions.exists():
            filtered_qs = task_actions.filter(end_time__isnull=True,parent__isnull=True,project_taskfiles__isnull=False).distinct().exclude(status__system_code__in = ['system_status_task_status_material_green','system_status_task_status_inspection_green'])
            task_action_count = filtered_qs.count()
            if filtered_qs.exists():
                url = reverse('admin:dashboard_taskactionlist_changelist') + '?project_id={}'.format(obj.pk)
                link_html = "<a class='btn bgc-white btn-light-secondary mx-0' href={}><span class='badge badge-secondary'>{}</span>&nbsp;<i class='fa fa-flag text-100'></i></a>".format(url, task_action_count)
                return format_html(link_html)
            else:
                url = reverse('admin:dashboard_rectifiedflag_changelist') + '?project_id={}'.format(obj.pk)
                link_html = "<a class='btn bgc-white btn-light-secondary mx-0' href={}><span class='badge badge-secondary'>{}</span>&nbsp;<i class='fa fa-flag text-100'  style=\"color:green\"></i></a>".format(url, task_action_count)
                return format_html(link_html)
        else:
            return 0

    get_flags.admin_order_field  = 'project_taskactions'  #Allows column order sorting
    get_flags.short_description = 'Flags'  #Renames column head


    def task_progress(self, obj):
        return f"{obj.progress_actual} %"# replace with your calculation
    task_progress.admin_order_field = 'progress_actual'
    task_progress.short_description = 'Progress'
   

    def get_project_station(self, obj):
        return obj.city
    get_project_station.admin_order_field = 'city'
    get_project_station.short_description = 'STA'

    
    def get_created_on(self, obj):
        return obj.created_on
    get_created_on.admin_order_field = 'created_on'
    get_created_on.short_description = 'Proj Start Date'

    def get_updated_on(self, obj):
        return obj.updated_on
    get_updated_on.admin_order_field = 'updated_on'
    get_updated_on.short_description = 'Proj Completion Date'

    def get_project_contractor(self, obj):
        return obj.contractor
    get_project_contractor.admin_order_field = 'contractor'
    get_project_contractor.short_description = 'Contr'

    def project_reference_number(self, obj):
        return obj.reference_number # replace with your calculation
    project_reference_number.admin_order_field = 'reference_number'
    project_reference_number.short_description = 'Ref CA'

    def progress_difference(self, obj):
        # Calculate the difference between progress_actual and progress_planned
        if obj.progress_planned:
            difference = obj.progress_actual - obj.progress_planned
            # Return the difference with a sign prefix
            return f"{'Lag' if difference < 0 else 'Lead'}:{abs(difference)}%"
        elif obj.progress_actual:
            return f"{'Lead'}:{abs(obj.progress_actual)}%"
        else:
            return "Update Project Progress"

    # Set the progress_difference method as a read-only field
    progress_difference.short_description = 'Lag/Lead'
    progress_difference.admin_order_field = 'progress_actual'

    fieldsets = (
        ('User & Groups Info', {
            'fields': (('users', 'groups'))
        }),
        ('Organization Info', {
            'fields': (('region','city','type'),('organization','thumbnail'))
        }),
        ('Project Info', {
            'fields': (('name','code'), ('contractor','consultant_name', 'contract_status','expenditure_total'), 'category', 'status','start_date', 'end_date', 'project_remarks')
        }),
    )
    search_fields = ('name','code','contract_status', 'created_on', 'updated_on')
    

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
            
        if db_field.name == "status":
            kwargs["queryset"] = SystemStatus.objects.filter(parent__system_code__in =['system_status_project_status']) #kwargs['disabled'] = True
    
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

     # Selected Filter Helper  Function
    def selectedFilter(self):
        formatted_string = ""
        if 'flag_id' in self.request.GET:
            flag_id = self.request.GET.get('flag_id',None)
            task_status = TaskStatus.objects.filter(id = flag_id).first()
            formatted_string = formatted_string + str(task_status.parent.name) + " > " + str(task_status.name) +" > "
        
        if 'city_id' in self.request.GET:
            city_id = self.request.GET.get('city_id',None)
            city = City.objects.filter(id = city_id).first()
            formatted_string = formatted_string + str(city.region.name) + " > " + str(city.name) + " > "

        if 'region_id' in self.request.GET:
            region_id = self.request.GET.get('region_id',None)
            region = Region.objects.filter(id = region_id).first()
            formatted_string = formatted_string + str(region.name) + " > "
        
        if 'inspection_id' in self.request.GET:
            inspection_id = self.request.GET.get('inspection_id',None)
            inspection = SystemStatus.objects.filter(id = inspection_id).first()
            formatted_string = formatted_string + str(inspection.name) + " > "
        
        if 'drf__created_on__gte' and 'drf__created_on__lte' in self.request.GET.keys():
            drf__created_on__gte = self.request.GET.get('drf__created_on__gte',None)
            drf__created_on__lte = self.request.GET.get('drf__created_on__lte',None)
            formatted_string = formatted_string + str(drf__created_on__gte) + "  To  " + str(drf__created_on__lte) + ">"

        return formatted_string
    
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
        project_qs = qs
        # project_regions = Region.objects.filter(id__in = filtered_region_rolebased(request,qs)).order_by('ordering')
        # project_cities = City.objects.filter(id__in = filtered_city_rolebased(request,qs))
        
        project_regions = Region.objects.filter(status = "active").order_by('ordering')
        project_cities = City.objects.filter(status = "active")
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

        # Region Card Filter
        region_counts = []
        region_counts_total = 0

        for region in project_regions:
            if 'drf__created_on__gte' in request.GET and 'drf__created_on__lte' in request.GET:
                count = Project.objects.filter(region=region,created_on__date__gte = request.GET['drf__created_on__gte'],created_on__date__lte = request.GET['drf__created_on__lte']).exclude(status__system_code__in = ['system_status_task_status_material_green','system_status_task_status_inspection_green']).count()
            else:
                count = Project.objects.filter(region=region).exclude(status__system_code__in = ['system_status_task_status_material_green','system_status_task_status_inspection_green']).count()

            region_counts_total = region_counts_total + count
            data_dict = {
                "id":str(region.id),
                "region_name":region.name,
                "region_count":count
            }
            region_counts.append(data_dict)
        extra_context['region_counts'] = list(region_counts)
        extra_context['region_counts_total'] = int(region_counts_total)

        # Station Card Filter
        cities_counts = []
        city_counts_total = 0

        
        if 'region_id' in request.GET:
            project_cities = project_cities.filter(region_id = request.GET['region_id'])
        
        elif 'city_id' in request.GET:
            project_cities = project_cities.filter(id = request.GET['city_id'])
       
        for city in project_cities:
            if 'drf__created_on__gte' in request.GET and 'drf__created_on__lte' in request.GET:
                count = Project.objects.filter(city=city,created_on__date__gte = request.GET['drf__created_on__gte'],created_on__date__lte = request.GET['drf__created_on__lte']).exclude(status__system_code__in = ['system_status_task_status_material_green','system_status_task_status_inspection_green']).count()
            else:
                count = Project.objects.filter(city=city).exclude(status__system_code__in = ['system_status_task_status_material_green','system_status_task_status_inspection_green']).count()
            city_counts_total = city_counts_total + count
            data_dict = {
                "id":str(city.id),
                "region_id":str(city.region.id),
                "city_name":city.name,
                "city_count":count
            }
            cities_counts.append(data_dict)

        extra_context['cities_counts'] = list(cities_counts)
        extra_context['city_counts_total'] = city_counts_total
        extra_context['selected_filters'] = self.selectedFilter()

        # Projects Financial Details
        weekly_obsns_qs = weekly_obsns_datefilter(request,tasks_action_qs)
        total_expenditure = project_qs.aggregate(Sum('expenditure_total'))['expenditure_total__sum']
        total_disbursement = project_qs.aggregate(Sum('disbursement_total'))['disbursement_total__sum']
        extra_context['projects_total_expenditure'] = total_expenditure
        extra_context['projects_disbursement_total'] = total_disbursement
        if total_expenditure and total_disbursement:
            extra_context['projects_remaining_total'] = total_expenditure - total_disbursement
        else:
            extra_context['projects_remaining_total'] = None

        extra_context['project_task_action_inspection'] = tasks_action_qs.filter(status__parent__system_code = 'system_status_task_status_material').values('status__name','status__color').annotate(Count('status'))
        extra_context['project_task_action_material'] = tasks_action_qs.filter(status__parent__system_code = 'system_status_task_status_inspection').values('status__name','status__color').annotate(Count('status'))
    
        extra_context['project_regions'] = project_regions
        extra_context['project_cities'] = project_cities.order_by('region__ordering')
        extra_context['weekly_obsns'] = weekly_obsns_qs
        extra_context['tasks_actions'] = tasks_action_qs
        extra_context['selected_filters'] = self.selectedFilter()
     
        """ CS Admin 23-9-22"""
        inspection_flags = SystemStatus.objects.filter(parent__system_code='system_status_task_status',status='active')
        extra_context['inspection_flags'] = inspection_flags


        # Totals
        extra_context['total_projects'] = qs.count()
        extra_context['qs'] = qs

        # Pie Chart for Inspection Flags
        dataset_inspection = tasks_action_qs.filter(status__parent__system_code__in = ["system_status_task_status_material","system_status_task_status_inspection"]).values('status__name','status__color').annotate(Count('status'))
        insp_labels = list()
        insp_data = list()
        insp_backgroundColor = list()
        # survived_series = list()
        # not_survived_series = list()

        for entry in dataset_inspection:
            insp_labels.append(entry['status__name'])
            insp_data.append(entry['status__count'])
            insp_backgroundColor.append(entry['status__color'])
            # survived_series.append(entry['survived_count'])
            # not_survived_series.append(entry['not_survived_count'])
        extra_context['insp_labels'] = insp_labels
        extra_context['insp_data'] = insp_data
        extra_context['insp_backgroundColor'] = insp_backgroundColor
        extra_context['req'] = request
        
        region_extra_rows = 0
        region_extra_overflow = False

        if project_regions.count() == project_cities.count():
            if project_regions.count() < 6:
                region_extra_rows = 5 - project_regions.count()

        if project_regions.count() > project_cities.count():
            if project_regions.count() < 6:
                region_extra_rows = 5 - project_regions.count()


        elif project_regions.count() < project_cities.count():
            if project_regions.count() < 6:
                region_extra_rows = 5 - project_regions.count()


        if (project_regions.count() + region_extra_rows) > 5:
            region_extra_overflow = True        


        if region_extra_rows > 0:
            extra_context['region_extra_rows'] = range(0, region_extra_rows)
        else:
            extra_context['region_extra_rows'] = range(0, region_extra_rows)

        extra_context['region_extra_overflow'] = region_extra_overflow
        
       
        cities_extra_rows = 0
        cities_extra_overflow = False
        if project_regions.count() == project_cities.count():
            if project_cities.count() < 6:
                cities_extra_rows = 5 - project_cities.count()

        if project_regions.count() > project_cities.count():
            if project_cities.count() < 6:
                cities_extra_rows = 5 - project_cities.count()


        elif project_regions.count() < project_cities.count():
            if project_cities.count() < 6:
                cities_extra_rows = 5 - project_cities.count()

        if (project_cities.count() + cities_extra_rows) > 5:
            cities_extra_overflow = True

        if cities_extra_rows > 0:
            extra_context['cities_extra_rows'] = range(0, cities_extra_rows)
        else:
            extra_context['cities_extra_rows'] = range(0, cities_extra_rows)

        extra_context['cities_extra_overflow'] = cities_extra_overflow

        # Graphs
        # Zone Wise Graph
        # Get all region names
        region_names = qs.values_list('region__name', flat=True)
        # Count occurrences of each region
        region_counts = Counter(region_names)
        result = [{'name': name, 'y': count} for name, count in region_counts.items()]
        extra_context['zonewise_graph_data'] = result

        # Station Wise Graph
        # Get all station names
        station_names = qs.values_list('city__name', flat=True)
        # Count occurrences of each region
        station_counts = Counter(station_names)
        result = [{'name': name, 'y': count} for name, count in station_counts.items()]
        extra_context['stationwise_graph_data'] = result
        return super(ReportAdmin, self).changelist_view(request, extra_context=extra_context)


    # This will help you to disable delete functionaliyt
    def get_queryset(self, request):
        qs = self.model._default_manager.get_queryset()
        # qs = qs.filter(region__in=request.user)
        project_ids_list = filtered_qs_rolebased(request,qs)
        qs = qs.filter(id__in = project_ids_list)
            # TODO: this should be handled by some parameter to the ChangeList.
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs.order_by('-created_on','-updated_on')
    
    
    
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser == 0:
            return True
        else:
            return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser == 0:
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

admin.site.register(Report,ReportAdmin)
