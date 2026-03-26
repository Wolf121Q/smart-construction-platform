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
from datetime import datetime
from django.template.response import TemplateResponse
from django.db.models import Count
from datetime import datetime
from django.utils.safestring import mark_safe
from notifications.signals import notify
from dashboard.utils.filterUserBasedQs import weekly_obsns_datefilter,filtered_qs_rolebased,filtered_region_rolebased,filtered_city_rolebased
from daterange_filter.filter import DateRangeFilter
from core.models import SystemType,UserTypeHierarchy
from project.models import Project

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

class ProjectDirectorHousingAdmin(admin.ModelAdmin):
    # change_list_template = 'admin/dashboard/change_list.html'
    #change_form_template = 'admin/dashboard/change_form.html'
    
    change_list_template = 'change_list.html'
    # change_form_template = 'change_form.html'
    list_display_links = None
    # list_display = ('reference_number','name', 'get_flags','progress_actual','consultant_name')
    readonly_fields = ('get_flags',)
    show_full_result_count = False
    list_filter = (('created_on',DateRangeFilter),RegionFilter,CityFilter,'project__organization')
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
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        self.request = request
        extra_context = extra_context or {}

        # Project's QS
        project_qs =  Project.objects.filter(id__in = filtered_qs_rolebased(request)).distinct()
        project_regions = Region.objects.filter(id__in = filtered_region_rolebased(request,project_qs),status = "active").order_by('ordering')
        project_cities = City.objects.filter(id__in = filtered_city_rolebased(request,project_qs),status = "active")

        # Filter Qs Based On the Region & Cities
        qs = qs.filter(project_id__in = filtered_qs_rolebased(request),
            project__region__id__in=project_regions.values_list('id', flat=True).distinct(),
            project__city__id__in=project_cities.values_list('id', flat=True).distinct())
        #        ,end_time__isnull=True,parent__isnull=True).exclude(status__system_code__in = ['system_status_task_status_material_green','system_status_task_status_inspection_green'])

        unique_task_action_ids = TaskFile.objects.values('task_action_id').distinct()
        # Region Card Filter
        region_counts = []
        region_counts_total = 0

        for region in project_regions:
            if 'drf__created_on__gte' in request.GET and 'drf__created_on__lte' in request.GET:
                count = qs.filter(project__region=region,created_on__date__gte = request.GET['drf__created_on__gte'],created_on__date__lte = request.GET['drf__created_on__lte'],end_time__isnull=True,parent__isnull=True).exclude(status__system_code__in = ['system_status_task_status_material_green','system_status_task_status_inspection_green']).count()
            else:
                count = qs.filter(project__region=region,end_time__isnull=True,parent__isnull=True).exclude(status__system_code__in = ['system_status_task_status_material_green','system_status_task_status_inspection_green']).count()
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

        
        if 'project__region_id' in request.GET:
            project_cities = project_cities.filter(region_id = request.GET['project__region_id'])
        
        elif 'project__city_id' in request.GET:
            project_cities = project_cities.filter(id = request.GET['project__city_id'])
       
        for city in project_cities:
            if 'drf__created_on__gte' in request.GET and 'drf__created_on__lte' in request.GET:
                count = qs.filter(project__city=city,created_on__date__gte = request.GET['drf__created_on__gte'],created_on__date__lte = request.GET['drf__created_on__lte'],end_time__isnull=True).exclude(status__system_code__in = ['system_status_task_status_material_green','system_status_task_status_inspection_green']).count()
            else:
                count = qs.filter(project__city=city,end_time__isnull=True,parent__isnull=True).exclude(status__system_code__in = ['system_status_task_status_material_green','system_status_task_status_inspection_green']).count()
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
        

        # Material Flag Card Filter
        material_flags_counts = []
        material_flags_counts_raised = 0
        material_flags_counts_cleared = 0
        material_flags_counts_balance = 0
        for mat_flag in SystemStatus.objects.filter(system_code = "system_status_task_status_material").first().get_descendants(include_self = False).exclude(system_code="system_status_task_status_material_green"):
            material_qs = qs.filter(status=mat_flag)
            # Start with a base queryset
            material_pending_qs = material_qs.filter(end_time__isnull=True,parent__isnull=True).exclude(status__system_code__in = ['system_status_task_status_material_green'])
            material_cleared_qs = material_qs.filter(Q(end_time__isnull=False)| Q(parent__isnull = False))
            material_raised_qs = material_pending_qs | material_cleared_qs
           
            material_flags_counts_raised = material_flags_counts_raised + material_raised_qs.count()
            material_flags_counts_cleared = material_flags_counts_cleared + material_cleared_qs.count()
            material_flags_counts_balance = material_flags_counts_balance + material_pending_qs.count()
            data_dict = {
                "id":str(mat_flag.id),
                "flag_color":mat_flag.color,
                "raised_count":material_raised_qs.count(),
                "cleared_count":material_cleared_qs.count(),
                "pending_count":material_pending_qs.count(),
            }
            
            if 'project__city_id' in request.GET:
               data_dict['url'] = "/dashboard/taskactionlist/?mat_flag_id={flag_id}&project__city_id={city_id}".format(flag_id = mat_flag.id,city_id = str(request.GET['project__city_id']))
            elif 'project__region_id' in request.GET:   
                data_dict['url'] = "/dashboard/taskactionlist/?mat_flag_id={flag_id}&project__region_id={region_id}".format(flag_id = mat_flag.id,region_id = str(request.GET['project__region_id']))
            else:
                data_dict['url'] = "/dashboard/taskactionlist/?mat_flag_id={flag_id}".format(flag_id = mat_flag.id)
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
        for ins_flag in SystemStatus.objects.filter(system_code = "system_status_task_status_inspection").first().get_descendants(include_self = False).exclude(system_code="system_status_task_status_inspection_green"):
            inspection_qs = qs.filter(status=ins_flag)
            inspection_pending_qs = inspection_qs.filter(end_time__isnull=True,parent__isnull=True).exclude(status__system_code__in = ['system_status_task_status_inspection_green'])
            inspection_cleared_qs = inspection_qs.filter(Q(end_time__isnull=False)| Q(parent__isnull = False) | Q(status__system_code='system_status_task_status_inspection_green'))
            inspection_raised_qs = inspection_pending_qs | inspection_cleared_qs
            
            inspection_flags_counts_raised =    inspection_flags_counts_raised + inspection_raised_qs.count()
            inspection_flags_counts_cleared =   inspection_flags_counts_cleared + inspection_cleared_qs.count()
            inspection_flags_counts_balance =   inspection_flags_counts_balance + inspection_pending_qs.count()
            data_dict = {
                "id":str(ins_flag.id),
                "flag_color":ins_flag.color,
                "raised_count":inspection_raised_qs.count(),
                "cleared_count":inspection_cleared_qs.count(),
                "pending_count":inspection_pending_qs.count()
            }
            
            if 'project__city_id' in request.GET:
               data_dict['url'] = "/taskactionlist/?ins_flag_id={flag_id}&project__city_id={city_id}".format(flag_id = ins_flag.id,city_id = str(request.GET['project__city_id']))
            elif 'project__region_id' in request.GET:   
                data_dict['url'] = "/taskactionlist/?ins_flag_id={flag_id}&project__region_id={region_id}".format(flag_id = ins_flag.id,region_id = str(request.GET['project__region_id']))
            else:
                data_dict['url'] = "/taskactionlist/?ins_flag_id={flag_id}".format(flag_id = ins_flag.id)

            inspection_flags_counts.append(data_dict)
        extra_context['ins_flag_counts'] = list(inspection_flags_counts)
        extra_context['inspection_flags_counts_raised'] = inspection_flags_counts_raised
        extra_context['inspection_flags_counts_cleared'] = inspection_flags_counts_cleared
        extra_context['inspection_flags_counts_balance'] = inspection_flags_counts_balance


        """ PIE CHART FOR SITE INSPECTION FLAGS """
        dataset_inspection_flag_pie = list(qs.filter(status__parent__system_code = 'system_status_task_status_inspection',end_time__isnull = True).exclude(status__system_code="system_status_task_status_inspection_green").order_by('status__name').values('status__name').annotate(status__color = F(name = 'status__color'),y = Count('status')))
        dataset_inspection_flag_pie_color = list()
        for entry in dataset_inspection_flag_pie:
            dataset_inspection_flag_pie_color.append(entry['status__color'])

        extra_context['dataset_inspection_flag_pie'] = dataset_inspection_flag_pie
        extra_context['dataset_inspection_flag_pie_color'] = dataset_inspection_flag_pie_color
        
        """ PIE CHART FOR SITE MATERIAL FLAGS """
        dataset_material_flag_pie = list(qs.filter(status__parent__system_code = 'system_status_task_status_material',end_time__isnull = True).exclude(status__system_code="system_status_task_status_material_green").order_by('status').values('status__name').annotate(status__color = F('status__color'),name=F('status__name'),y = Count('status')))
        dataset_material_flag_pie_color = list()
        for entry in dataset_material_flag_pie:
            dataset_material_flag_pie_color.append(entry['status__color'])
    
        extra_context['dataset_material_flag_pie'] = dataset_material_flag_pie
        extra_context['dataset_material_flag_pie_color'] = dataset_material_flag_pie_color

         ####### Pie Chart for Inspection Flags #######
        dataset_flag_pie = list(qs.values('status__color',name = F('status__name')).annotate(y = Count('status')))
        dataset_flag_pie_color = list()
        for entry in dataset_flag_pie:
            dataset_flag_pie_color.append(entry['status__color'])
        
        ####### Pie Chart For RegionWise Distribution Of Projects #######
        region_data = list(qs.exclude(status__system_code__in = ['system_status_task_status_material_green','system_status_task_status_inspection_green']).order_by('project__region__ordering').values(('project__region__name')).distinct().annotate(name = F('project__region__name'),y = Count('id')))
        extra_context['dataset_inspection'] = dataset_flag_pie
        extra_context['dataset_region'] = region_data
        extra_context['dataset_color'] = dataset_flag_pie_color
   
        ####### END BAR CHART FOR MATERIAL AND INSPECTION FLAGS ###############
        return super(ProjectDirectorHousingAdmin, self).changelist_view(request, extra_context=extra_context)

    # def get_queryset(self, request):
    #     qs = self.model._default_manager.get_queryset().filter(project_id__in = filtered_qs_rolebased(request),end_time__isnull=True).order_by("-created_on")
    #     combined_queryset = self.model.objects.none()
    #     time_line_obj = TaskActionTimeLine.objects.filter(user_type = request.user.type).first()
    #     if time_line_obj:
    #         time_line = datetime.now() - time_line_obj.time_line
    #         if time_line_obj.flag_type.all().count() > 0:
    #             for type in time_line_obj.flag_type.all():
    #                 qs = qs.exclude(status__type__system_code = type.system_code)
    #                 combined_queryset = combined_queryset | self.model._default_manager.get_queryset().filter(status__type__system_code = type.system_code,created_on__date__lt = time_line.date(),)
    #             qs = qs | combined_queryset
    #             qs = qs.order_by("-created_on")
    #         else:
    #             qs = qs
    #     else:
    #         qs = qs
    #     ordering = self.get_ordering(request)
    #     if ordering:
    #         qs = qs.order_by(*ordering)
        

        # Filter your queryset and use distinct() to get unique instances based on the primary key
        # qs = qs.filter(
        #     end_time__isnull=True,
        #     parent__isnull=True,
        #     project_taskfiles__isnull=False
        # ).exclude(
        #     Q(status__system_code='system_status_task_status_material_green') |
        #     Q(status__system_code='system_status_task_status_inspection_green')
        # ).order_by('-created_on').select_related('project_taskfiles').distinct('pk')

        # Get unique task_action_id values from TaskFile
        # unique_task_action_ids = TaskFile.objects.values('task_action_id').distinct()
        # # Start with a base queryset
        # qs = qs.filter(
        #     id__in = unique_task_action_ids,
        #     end_time__isnull=True,
        # ).exclude(
        #     Q(status__system_code='system_status_task_status_material_green') |
        #     Q(status__system_code='system_status_task_status_inspection_green')
        # ).order_by('-created_on')
        # return qs.filter(end_time__isnull=True,parent__isnull=True).order_by('-created_on')

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
 
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            # CS Admin
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
            # path('comment_replay/', self.readJson, name='pdh_comment_reply'),
        #     path('comment_replay1/', self.readJson1, name='pdh_comment_reply1'),
        ]
        return my_urls + urls

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
            if task_action_obj.end_time is not None:
                # It has children, let's find one with end_time as null
                child_with_null_end_time = task_action_obj.get_children().filter(end_time__isnull=True).first()
                if child_with_null_end_time:
                    task_action = child_with_null_end_time
                else:
                    task_action = task_action_obj
            else:
                task_action = task_action_obj
            
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
    
    def get_quill(self,value):
        return '{"delta":{"ops":[{"insert":"test"}]},"html":"'+value+'"}'

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request):
        return False
        if request.user.is_superuser == 0:
            return False
        else:
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
        # if not obj.created_by:
        #     # Only set added_by during the first save.
        #     obj.created_by = request.user
        # else:
        #     obj.updated_by = request.user
        obj.ip = get_client_ip(request)
        super().save_model(request, obj, form, change)

admin.site.register(ProjectDirectorHousing, ProjectDirectorHousingAdmin)