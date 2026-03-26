from django.contrib import admin
from core.submodels.SystemStatus import SystemStatus
from dashboard.models import ProjectDirectorHousing
from organization.models import City,Region
from project.models import Task,TaskAction,TaskActionComment,TaskFile
from project.submodels.TaskStatus import TaskStatus
from utils.IP import get_client_ip
from django.contrib.admin import SimpleListFilter
from django.db.models import Subquery,Sum
from django.urls import re_path
from django.http import HttpResponse,JsonResponse
from dashboard.serializers import UserSerializer,TaskActionSerializer,TaskFileSerializer
from django.views.decorators.csrf import csrf_exempt
from core.models import User
from django.shortcuts import render
from datetime import datetime, timedelta
from datetime import datetime
from django.template.response import TemplateResponse
from django.db.models import Count
from datetime import datetime
from django.utils.safestring import mark_safe
from notifications.signals import notify
from dashboard.utils.filterUserBasedQs import weekly_obsns_datefilter,filtered_qs_rolebased,filtered_region_rolebased,filtered_city_rolebased
from daterange_filter.filter import DateRangeFilter
from core.models import SystemType
import traceback

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
            # return queryset.filter(project_taskactions__status__id=self.value())

class ProjectDirectorHousingAdmin(admin.ModelAdmin):
    # change_list_template = 'admin/dashboard/change_list.html'
    #change_form_template = 'admin/dashboard/change_form.html'
    
    change_list_template = 'change_list.html'
    change_form_template = 'change_form.html'
    list_display_links = None
    list_display = ('reference_number','name', 'get_flags','consultant_name','contractor_name')
    readonly_fields = ('get_flags',)
    show_full_result_count = False
    list_filter = (RegionFilter,CityFilter,FlagsFilter,InspectionFilter,('project_taskactions__created_on',DateRangeFilter))
    list_per_page = 5
    # search_fields = ('code','name', 'consultant_name','contractor_name','status__name', 'start_date', 'end_date')
    ordering = ('name','code','status', 'created_on', 'updated_on')

    def get_flags(self, obj,inspection_id = None,flag_id = None):
        flag_id = self.request.GET.get('flag_id', None)
        if flag_id is not None:
            if obj.project_taskaction_related is not None:
                if flag_id:
                    filtered_qs = obj.project_taskaction_related.filter(status_id=flag_id,end_time__isnull = True)
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

        # Base Querysets
        project_qs = qs
        project_regions = Region.objects.filter(id__in = filtered_region_rolebased(request,qs)).order_by('ordering')
        project_cities = City.objects.filter(id__in = filtered_city_rolebased(request,qs))
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
   
        return super(ProjectDirectorHousingAdmin, self).changelist_view(request, extra_context=extra_context)

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
        return qs
       

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
        
        if 'drf__created_on__gte' and 'drf__created_on__lte' in self.request.GET.keys():
            drf__created_on__gte = self.request.GET.get('drf__created_on__gte',None)
            drf__created_on__lte = self.request.GET.get('drf__created_on__lte',None)
            formatted_string = formatted_string + str(drf__created_on__gte) + "  To  " + str(drf__created_on__lte) + "/"

        return formatted_string
 
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            # CS Admin
            re_path(r'^task_action_flag_detail/$', self.get_task_action_flag_detail,name='task_action_flag_detail'),
            re_path(r'^task_action_first_attachment/$', self.task_action_first_attachment,name='task_action_flag_detail'),
            re_path(r'^task_action_chat_detail/$', self.get_task_action_chat_detail,name='task_action_chat_detail'),

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
    def task_action_first_attachment(self,request):
        if request.method == 'POST':
            id = request.POST.get("id",None)
            task_action_comment = TaskActionComment.objects.filter(task_action_id = id,parent__isnull = True).first()
            task_action_files = TaskFile.objects.filter(task_action_comment_id=task_action_comment.id)
            data = {'task_action_comment': task_action_comment,'task_action_files':task_action_files}
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
            task_action_comments = TaskActionComment.objects.filter(task_action_id=task_action_id).order_by('created_on')
            #task_action_files = TaskFile.objects.filter(task_action_id=task_action_id)
            data = {}
            data['task_id'] = task_action.task.id
            data['task_action'] = task_action
            data['task_action_comments'] = task_action_comments
            return TemplateResponse(request, 'partials/chat_box_body.html', data)

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
            user_id = request.POST.get('tagged_user_id',None)
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

                task_action_comment.description = self.get_quill(comment)
                task_action_comment.status = task_action.status
                task_action_comment.save()
        
                # Creating New Notification
                if user_id:
                    sender = User.objects.get(id=request.user.id)
                    receiver = User.objects.get(id=user_id)
                    notify.send(sender, recipient=receiver,action_object= task_action_comment, verb='Message', description=request.POST.get('comment'))

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


                data = {'status': 1, 'data': {'msg': 'Created Successfully'},'id':str(task_action.id)}
                return JsonResponse(data)
            else:
                data = {'status': 1, 'data': {'msg': 'Created Successfully'},'id':str(task_action.id)}
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