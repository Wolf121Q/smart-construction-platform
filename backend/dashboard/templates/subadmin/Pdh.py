import operator
from re import search
from django.utils.six.moves import reduce
from django.db.models import Q
from django.contrib import admin
from core.submodels.SystemStatus import SystemStatus
from dashboard.models import Pdh
from organization.submodels.Organization import Organization
from project.models import Project,Task,TaskAction,TaskActionComment
from project.submodels.Category import Category
from project.submodels.TaskStatus import TaskStatus
from utils.IP import get_client_ip
from django.db.models import Count
from django.db.models import Subquery
from django.contrib.admin import SimpleListFilter
from django.db.models import Sum
from django.urls import re_path,path
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from core.models import User
from django.views.decorators.csrf import csrf_exempt
from dashboard.serializers import UserSerializer
from django.conf import settings
from project.models import Project
from utils.CityToCountry import CityToCountry
from organization.models import Type

class StatusFilter(SimpleListFilter):
    title = 'Status' # or use _('country') for translated title
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        # statuses = set([c.status for c in model_admin.model.objects.order_by('status__system_code').distinct('status__system_code')])
        statuses =  set([c.status for c in model_admin.model.objects.filter(status__parent__system_code ='system_status_project_status')])
        return [(c.id, c.name) for c in statuses]
    def queryset(self, request, queryset):

        if self.value():
            return queryset.filter(status__id__exact=self.value())

class CityFilter(SimpleListFilter):
    title = 'City' # or use _('country') for translated title
    parameter_name = 'City'

    def lookups(self, request, model_admin):
        # statuses = set([c.status for c in model_admin.model.objects.order_by('status__system_code').distinct('status__system_code')])
        cities =  set([c.city for c in model_admin.model.objects.order_by('city__code').distinct('city__code')])
        return [(c.id, c.name) for c in cities]
    def queryset(self, request, queryset):

        if self.value():
            return queryset.filter(city__id__exact=self.value())

class PdhAdmin(admin.ModelAdmin):
    change_list_template = 'admin/dashboard/change_list.html'
    change_form_template = 'admin/dashboard/change_form.html'
    
    list_display = ('serial_number','code','name', 'consultant_name','contractor_name', 'start_date', 'end_date')
    # list_display_links = ('indented_title',)
    list_filter = (StatusFilter,CityFilter,)
    list_per_page = 10
    search_fields = ('serial_number','code','name', 'consultant_name','contractor_name','status__name', 'start_date', 'end_date')
    ordering = ('serial_number','name','code','status', 'created_on', 'updated_on')
    # This will help you to disable delete functionaliyt
    
    def changelist_view(self, request, extra_context=None):
        global project_qs
        #inspection_flags = SystemStatus.objects.get(system_code='system_status_task_status').get_descendants(include_self=False).filter(status='active')
        project_qs = Project.objects.filter(organization__region__users = request.user)
        tasks_qs = Task.objects.filter(project_id__in=Subquery(project_qs.values('id')))
        tasks_action_qs = TaskAction.objects.filter(task_id__in=Subquery(tasks_qs.values('id')))

        if 'City' in request.GET.keys():
            city_id = request.GET.get('City',None)
            project_qs = project_qs.filter(city_id = city_id)
            tasks_qs = tasks_qs.filter(project_id__in=Subquery(project_qs.values('id')))
            tasks_action_qs = tasks_action_qs.filter(task_id__in=Subquery(tasks_qs.values('id')))

        if 'q' in request.GET.keys():
            query_param = request.GET.get('q', None)
            if query_param in ['Mat','Ins']:
                if query_param == 'Mat':
                    tasks_qs = tasks_action_qs.filter(status__parent__system_code = 'system_status_task_status_material')
                    project_qs = project_qs.filter(id__in = Subquery(tasks_qs.values('project_id')))
                elif query_param == 'Ins':
                    tasks_qs = tasks_action_qs.filter(status__parent__system_code = 'system_status_task_status_inspection')
                    project_qs = project_qs.filter(id__in = Subquery(tasks_qs.values('project_id')))

            elif query_param in ['Mat-Yellow','Mat-Red','Mat-Brown','Mat-Green']:
                query_param = query_param.replace("Mat-","")
                query_param = query_param[0].lower() + query_param[1:]
                system_status = "system_status_task_status_material_"+ str(query_param)
                tasks_qs = tasks_action_qs.filter(status__parent__system_code = 'system_status_task_status_material',status__system_code = system_status)
                project_qs = project_qs.filter(id__in = Subquery(tasks_qs.values('project_id')))

            elif query_param in ['Ins-Yellow','Ins-Red','Ins-Brown','Ins-Green']:
                query_param = query_param.replace("Mat-","")
                query_param = query_param[0].lower() + query_param[1:]
                system_status = "system_status_task_status_material_"+ str(query_param)
                tasks_qs = tasks_action_qs.filter(status__parent__system_code = 'system_status_task_status_inspection',status__system_code = system_status)
                project_qs = project_qs.filter(id__in = Subquery(tasks_qs.values('project_id')))


        response = super(PdhAdmin, self).changelist_view(request, extra_context)
        extra_context = extra_context or {}
        extra_context['inspection_flags'] = SystemStatus.objects.filter(parent__system_code='system_status_task_status',status='active')
        extra_context['projects'] = project_qs
        extra_context['project_count'] = project_qs.count()
        extra_context['total_projects_cost'] = project_qs.aggregate(Sum('expenditure_total'))
        extra_context['total_projects_cost_ongoing'] = project_qs.filter(status__system_code = 'system_status_project_status_valid').aggregate(Sum('expenditure_total'))
        extra_context['total_projects_cost_completed'] = project_qs.filter(status__system_code = 'system_status_project_status_completed').aggregate(Sum('expenditure_total'))
        extra_context['project_citywise'] = project_qs.values('city__id','city__name').annotate(Count('city'))
        extra_context['project_citywise_ongoing'] = project_qs.filter(status__system_code = 'system_status_project_status_valid').values('city__name').annotate(Count('city'))
        extra_context['project_citywise_completed'] = project_qs.filter(status__system_code = 'system_status_project_status_completed').values('city__name').annotate(Count('city'))
        extra_context['project_status'] = project_qs.values('status__color').annotate(task_flag = Count('status'))
        extra_context['project_parent_status'] = project_qs.values('status__parent__name').annotate(Count('status__parent__name'))
        extra_context['project_task_action_count'] = tasks_action_qs.count()
        extra_context['project_task_action_inspection'] = tasks_action_qs.filter(status__parent__system_code = 'system_status_task_status_material').values('status__name','status__color').annotate(Count('status'))
        extra_context['project_task_action_material'] = tasks_action_qs.filter(status__parent__system_code = 'system_status_task_status_inspection').values('status__name','status__color').annotate(Count('status'))

        # extra_context['project_task_count'] = tasks_qs.count()
        # extra_context['project_task_inspection'] = tasks_qs.filter(status__parent__system_code = 'system_status_task_status_inspection').values('status__color','status__name').annotate(Count('status'))
        # extra_context['project_task_material'] = tasks_qs.filter(status__parent__system_code = 'system_status_task_status_material').values('status__color').annotate(Count('status'))
        

        #print(tasks_action_qs.filter(status__parent__system_code = 'system_status_task_status_material').values('status__name','status__color').annotate(Count('status'))) 
        ### Charts Data ###
        pie_chart_data = []
        colors = []
        for task_action in tasks_action_qs:
            if task_action.status:
                if task_action.status.color not in colors:
                    colors.append(task_action.status.color)

        chart_data = tasks_action_qs.values('status__name').annotate(Count('status'))
        for i in chart_data:
            oldkeys = list(i.keys())
            newkeys = [s.replace('status__name', 'name') for s in oldkeys]
            newkeys = list(map(lambda x: x.replace('status__count', 'y'), newkeys))
            vals = list(i.values())
            newdictionary = {k: v for k, v in zip(newkeys, vals)}
            pie_chart_data.append(newdictionary)
    
        extra_context['colors'] = colors
        extra_context['pie_chart_data'] = pie_chart_data
        response.context_data.update(extra_context)
        return response


    def get_search_results(self, request, queryset, search_term):
        # search_term is what you input in admin site
        # queryset is search results
        queryset, use_distinct = super(PdhAdmin, self).get_search_results(request, queryset, search_term)
        queryset = project_qs
        return queryset, use_distinct
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['tasks'] = Task.objects.filter(project_id = object_id)
        extra_context['task_action'] = TaskAction.objects.all().first()
        if TaskActionComment.objects.exists():
            extra_context['task_action_comment'] = TaskActionComment.objects.filter(task_action_id = TaskAction.objects.all().first().id).first()
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            re_path(r'^pdh_task_detail/(?P<id>\d+)/$', self.getPdhTaskDetail, name='pdh_task_detail'),
            path('comment_replay/', self.readJson, name='pdh_comment_reply'),
            path('comment_replay1/', self.readJson1, name='pdh_comment_reply1'),
        ]
        return my_urls + urls

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
                        return render(request, 'admin/dashboard/pdh/pdh_task_detail.html',data)
                    else:
                        return HttpResponse("Sorry! Data Not Founded")
                return HttpResponse("Sorry! Data Not Founded1")
            return HttpResponse("Sorry! Your Role not Allowed")
        return HttpResponse("Sorry! Method not Allowed")
        
    

    ##### START UTIL FUNCTIONS ##########  

    @csrf_exempt
    def readJson(self,request):
        import os
        import json
        static_path = str(settings.STATICFILES_DIRS[0])
        with open(os.path.join(static_path +'/ProjJSON.json'), 'r') as f:
            data = json.load(f)
            for i in range(len(data['RECORDS'])):
                processed_dict = self.processDict(data['RECORDS'][i])
                project_obj = Project(**processed_dict)
                project_obj.save()
                print("Project Created Successfully",project_obj.id)
        return HttpResponse("HELLOW")




    def _dict_key_del(self,list_of_keys,dict_for_key_to_remove):
        for key in list_of_keys:
            if dict_for_key_to_remove.__contains__(key):
                del dict_for_key_to_remove[key]
        return dict_for_key_to_remove
    
    def processDict(self,dictionary):
        from datetime import timedelta, datetime
        p=['name','start_date','end_date','duration','project','created_by','updated_by','created_on','updated_on','progress_planned','progress_actual','start_date_actual','end_date_actual','time_lapsed_percentage','time_lapsed_date','is_type_umbrella','disbursement','disbursement_percentage','expenditure','expenditure_percentage','disbursement_total','expenditure_total','progress_planned_revised','disbursement_target','template','type','disbursement_usd','sector_id','name_short','consultant_name','contractor_name','category_code','phase_code','sector_code','contract_status','project_remarks','city','ask_or_dha','askari','ask_sector','code']
        e=dict(zip(p,list(dictionary.values())))

        list_of_keys = ['project_remarks','category_code','name_short','disbursement_usd','type','disbursement_target','progress_planned_revised','expenditure_percentage','expenditure','disbursement_percentage','disbursement','enddate_actual','startdate_actual','is_type_umbrella','time_lapsed_date','time_lapsed_percentage','end_date_actual','start_date_actual','progress_actual','progress_planned','sector_id','phase_code','sector_code','ask_or_dha','ask_sector','askari']
        processed_dict = self._dict_key_del(list_of_keys,e)

        # GEO DATA
        city = CityToCountry(processed_dict['city'])
        region = city.region

        user = User.objects.filter(username = 'qa_office').first()


        # datetime.datetime.strptime(processed_dict['start_date'].split(' ', 1)[0], "%d/%m/%Y").strftime("%Y-%m-%d")
        dict_for_update = {
            'created_by' : user,
            'updated_by' : user,
            'created_on' : datetime.strptime(processed_dict['created_on'].split(' ', 1)[0], "%d/%m/%Y").strftime("%Y-%m-%d"),
            'updated_on' : datetime.strptime(processed_dict['updated_on'].split(' ', 1)[0], "%d/%m/%Y").strftime("%Y-%m-%d"),
            'start_date' : datetime.strptime(processed_dict['start_date'].split(' ', 1)[0], "%d/%m/%Y").strftime("%Y-%m-%d"),
            'end_date' : datetime.strptime(processed_dict['end_date'].split(' ', 1)[0], "%d/%m/%Y").strftime("%Y-%m-%d"),
            'duration' : timedelta(days=int(processed_dict['duration'])),
            'city' : city,
            'region' : region,
            'category': Category.objects.all().first(),
            'organization': Organization.objects.all().first(),
            'status': SystemStatus.objects.filter(system_code = 'system_status_project_status_valid').first(),
            'type' : Type.objects.filter(code = 'DHA').first(),
        }

        # print(dict_for_update)
        processed_dict.update(dict_for_update)
        return processed_dict

    @csrf_exempt
    def readJson1(self,request):
        import os
        import json
        static_path = str(settings.STATICFILES_DIRS[0])
        with open(os.path.join(static_path +'/TaskJSON.json'), 'r') as f:
            data = json.load(f)
            for i in range(len(data['RECORDS'])):
                if not int(data['RECORDS'][i]['act_level']) in [0,2]:
                    print(data['RECORDS'][i]['act_level'])
                    print(data['RECORDS'][i]['actprojid'])
                    processed_dict1 = self.processDict1(data['RECORDS'][i])
                    task_obj = Task(**processed_dict1)
                    task_obj.save()
                    print("Task Created Successfully",task_obj.id)
        return HttpResponse("HELLOW")

    def _dict_key_del1(self,list_of_keys,dict_for_key_to_remove):
        for key in list_of_keys:
            if dict_for_key_to_remove.__contains__(key):
                del dict_for_key_to_remove[key]
        return dict_for_key_to_remove
    
    def processDict1(self,dictionary):
        from datetime import timedelta, datetime
        p=['act_id','name','start_date','end_date','duration','project','progress_planned','act_level','created_by','updated_by','created_on','updated_on']
        e=dict(zip(p,list(dictionary.values())))

        list_of_keys = ['act_id','act_level']
        processed_dict = self._dict_key_del1(list_of_keys,e)

        print(processed_dict)
        # User
        project = Project.objects.filter(serial_number = processed_dict['project']).first()
        user = User.objects.filter(username = 'qa_office').first()

        # datetime.datetime.strptime(processed_dict['start_date'].split(' ', 1)[0], "%d/%m/%Y").strftime("%Y-%m-%d")
        dict_for_update = {
            'created_by' : user,
            'updated_by' : user,
            'created_on' : datetime.strptime(processed_dict['created_on'].split(' ', 1)[0], "%d/%m/%Y"),
            'updated_on' : datetime.strptime(processed_dict['updated_on'].split(' ', 1)[0], "%d/%m/%Y"),
            'start_date' : datetime.strptime(processed_dict['start_date'].split(' ', 1)[0], "%d/%m/%Y"),
            'end_date' : datetime.strptime(processed_dict['end_date'].split(' ', 1)[0], "%d/%m/%Y"),
            'duration' : timedelta(days=int(processed_dict['duration'])),
            'project':project,
            'status': TaskStatus.objects.order_by('?').first(),
            'city' : project.city,
            'region' : project.region,
            'organization': project.organization,

            'code': str(dictionary['act_id'])+str(project.serial_number),
            'start_date_actual': datetime.strptime(processed_dict['start_date'].split(' ', 1)[0], "%d/%m/%Y"),
            'start_date_planned_revised': datetime.strptime(processed_dict['start_date'].split(' ', 1)[0], "%d/%m/%Y"),
            'end_date_actual': datetime.strptime(processed_dict['end_date'].split(' ', 1)[0], "%d/%m/%Y"),
            'end_date_planned_revised': datetime.strptime(processed_dict['end_date'].split(' ', 1)[0], "%d/%m/%Y"),
        }

        # print(dict_for_update)
        processed_dict.update(dict_for_update)
        return processed_dict

    ##### END UTIL FUNCTIONS ##########  
    
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False
        # if request.user.type.code == "system_type_user_region":
        #     return True
        # else:
        #     return False

    def has_change_permission(self, request, obj=None):
        if request.user.type.code == "system_type_user_region":
            return True
        else:
            return False

    def has_view_permission(self, request, obj=None):
        if request.user.type.code == "system_type_user_region":
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

admin.site.register(Pdh, PdhAdmin)