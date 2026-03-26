from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from core.models import SystemStatus,SystemType,AppVersion,UserProfile
from project.models import Project,Task,TaskAction,TaskFile
from project.api.login.authentication import SafeJWTAuthentication
from project.api.login.serializers import StatusSerializer,TypeSerializer,TaskFileSerializer,TaskSerializer,ProjectSerializer,TaskActionSerializer,OrganizationSerializer,CitySerializer,RegionSerializer,AppVersionSerializer
from project.utils.UpdateTaskAction import UpdateTaskAction,UpdateTasksProgress,UpdateProjectProgress
from organization.models import Organization,Region,City
from django.db.models import Q
from dashboard.utils.filterUserBasedQs import filtered_project_qs_rolebased_android,filtered_region_rolebased_android

import datetime

@api_view(['GET'])
@authentication_classes([SafeJWTAuthentication,])
def getStatuses(request):
    response = Response()
    response.data = {'status':0,'message':'Method is not allowed','data':{None}}
    if request.method == 'GET':
        if request.user.is_authenticated:
            system_status = SystemStatus.objects.get(system_code='system_status_task_status').get_descendants(include_self=False).filter(status='active')
            status_data = StatusSerializer(system_status, many=True).data

            # paginator = PageNumberPagination()
            # paginator.page_size = 2
            # result_page = paginator.paginate_queryset(system_status, request)
            # status_data = StatusSerializer(result_page, many=True).data


            response.data = {'status': 1, 'message': '', 'response_data': status_data}
    return response

@api_view(['GET'])
@authentication_classes([SafeJWTAuthentication,])
def getTypes(request):
    response = Response()
    response.data = {'status':0,'message':'Method is not allowed','data':{None}}
    if request.method == 'GET':
        if request.user.is_authenticated:
            system_status = SystemType.objects.get(system_code='system_type_task_type').get_descendants(include_self=False).filter(status='active')
            status_data = TypeSerializer(system_status, many=True).data

            response.data = {'status': 1, 'message': '', 'response_data': status_data}
    return response

@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
@authentication_classes([SafeJWTAuthentication,])
def getOrganizations(request):
    response = Response()
    response.data = {'status':0,'message':'Method is not allowed','response_data':None}
    if request.method == 'GET':
        if request.user.is_authenticated:
            organizations = Organization.objects.all().order_by('name')
            organizations_data = OrganizationSerializer(organizations,many=True).data
            response.data = {'status': 1, 'message': '', 'response_data': organizations_data}
            return response
    return response

@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
@authentication_classes([SafeJWTAuthentication,])
def getProjects(request):
    response = Response()
    response.data = {'status':0,'message':'Method is not allowed','response_data':None}
    if request.method == 'GET':
        if request.user.is_authenticated:
            # user_profile = UserProfile.objects.filter(user = request.user).first()
            # if user_profile:
            #     if user_profile.projects.exists():
            #         projects = user_profile.projects.all()
            #     else:
            #         projects = filtered_project_qs_rolebased_android(request)
            # else:
            projects = filtered_project_qs_rolebased_android(request)
            projects_data = ProjectSerializer(projects,many=True,context={'request': request}).data
            response.data = {'status': 1, 'message': '', 'response_data': projects_data}
            return response
    return response


@api_view(['GET'])
@authentication_classes([SafeJWTAuthentication,])
def getFlagAttachments(request):
    response = Response()
    response.data = {'status':0,'message':'Method is not allowed','data':{None}}
    if request.method == 'GET':
        if request.user.is_authenticated:
            task_action_id = request.GET.get("task_action_id",None)
            if task_action_id:
                task_files = TaskFile.objects.filter(task_action_id = task_action_id)
                task_files_data = TaskFileSerializer(task_files,many=True).data
                response.data = {'status': 1, 'message': '', 'response_data': task_files_data}
                return response
            else:
                response.data = {'status': 1, 'message': '', 'response_data': "Task Action Id not found"}
        else:
            response.data = {'status': 1, 'message': '', 'response_data': "User not allowed."}
    return response


@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
@authentication_classes([SafeJWTAuthentication,])
def getRegions(request):
    response = Response()
    response.data = {'status':0,'message':'Method is not allowed','response_data':None}
    if request.method == 'GET':
        if request.user.is_authenticated:
            regions = filtered_region_rolebased_android(request)
            regions_data = RegionSerializer(regions,many=True).data
            response.data = {'status': 1, 'message': '', 'response_data': regions_data}
            return response
    return response

@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
@authentication_classes([SafeJWTAuthentication,])
def getCities(request):
    response = Response()
    response.data = {'status':0,'message':'Method is not allowed','response_data':None}
    if request.method == 'GET':
        if request.user.is_authenticated:
            cities = City.objects.all().order_by('name')
            cities_data = CitySerializer(cities,many=True).data
            response.data = {'status': 1, 'message': '', 'response_data': cities_data}
            return response
    return response

@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
@authentication_classes([SafeJWTAuthentication,])
def getProjectTasks(request):
    response = Response()
    response.data = {'status':0,'message':'Method is not allowed','response_data':None}
    if request.method == 'GET':
        if request.user.is_authenticated:
            tasks = Task.objects.all()
            tasks_data = TaskSerializer(tasks,many=True,context={'request': request}).data

            # paginator = PageNumberPagination()
            # paginator.page_size = 3
            # result_page = paginator.paginate_queryset(tasks, request)
            # tasks_data = TaskSerializer(result_page, many=True).data

            response.data = {'status': 1, 'message': '', 'response_data': tasks_data}
            return response
    return response

@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
@authentication_classes([SafeJWTAuthentication,])
def getFlags(request):
    response = Response()
    response.data = {'status':0,'message':'Method is not allowed','response_data':None}
    if request.method == 'GET':
        if request.user.is_authenticated:
            flags = TaskAction.objects.filter(created_by = request.user)
            flags_data = TaskActionSerializer(flags,many=True).data

            # paginator = PageNumberPagination()
            # paginator.page_size = 3
            # result_page = paginator.paginate_queryset(tasks, request)
            # tasks_data = TaskSerializer(result_page, many=True).data

            response.data = {'status': 1, 'message': '', 'data_array': flags_data}
            return response
    return response

@api_view(['POST'])
@permission_classes([AllowAny])
# @csrf_protect
@csrf_exempt
@authentication_classes([SafeJWTAuthentication, ])
def UpdateProjectTasks(request):
    response = Response()
    response.data = {'status':0,'message':'Method is not allowed','data':{None}}
    if request.method == 'POST':
        if request.user.is_authenticated:
            response.data = UpdateTaskAction(request)
    return response

@api_view(['POST'])
@permission_classes([AllowAny])
# @csrf_protect
@csrf_exempt
@authentication_classes([SafeJWTAuthentication, ])
def UpdateProjectTasksProgress(request):
    response = Response()
    response.data = {'status':0,'message':'Method is not allowed','data':{None}}
    if request.method == 'POST':
        if request.user.is_authenticated:
            response.data = UpdateTasksProgress(request)
    return response


@api_view(['GET'])
@permission_classes([AllowAny])
# @csrf_protect
@csrf_exempt
def getAppVersion(request):
    response = Response()
    if request.method == 'GET':
        app = request.GET.get("app",None)
        if app:
            app_versions = AppVersion.objects.filter(type = app)
            app_version_data = AppVersionSerializer(app_versions,many=True).data
            if app_version_data:
                response.data = {'success':1,'message':'','data_array':app_version_data[0]}
            else:
                response.data = {'success':1,'message':'','data_array':app_version_data}
    else:
        response.data =  {'status':0,'message':'Method is not allowed','data':{None}}
    return response


def calculate_status_counts(task_action_data):
    status_counts = {}
    parent_status = None
    status_ids = [task.get('status', 'unknown') for task in task_action_data if task.get('status', 'unknown') != 'unknown']

    # Fetch all statuses in one query
    statuses = SystemStatus.objects.filter(id__in=status_ids)
    status_dict = {status.id: status for status in statuses}

    for status_id in status_ids:
        status = status_dict.get(status_id)
        if status:
            parent_status = status.parent
            # Use the status name as the key to avoid repetition
            if status.name in status_counts:
                # Increment quantity if the status is already in the counts
                status_counts[status.name]['quantity'] += 1
            else:
                # Add a new entry for the status if it's not in the counts
                status_counts[status.name] = {
                    'id': status.id,
                    'name': status.name,
                    'quantity': 1,
                    'color': status.color,
                }

    # Second loop: Include all possible statuses, even if they have a quantity of 0
    if parent_status:
        ordered_status_counts = {}
        all_statuses = SystemStatus.objects.filter(parent=parent_status)
        for status in all_statuses:
            ordered_status_counts[status.name] = status_counts.get(status.name, {
                'id': status.id,
                'name': status.name,
                'quantity': 0,
                'color': status.color,
            })

        # Update status_counts with the ordered dictionary
        status_counts.clear()
        status_counts.update(ordered_status_counts)

    # Convert the status_counts dictionary to a list
    status_list = list(status_counts.values())
    return status_list


@api_view(['GET'])
@permission_classes([AllowAny])
# @csrf_protect
@csrf_exempt
def getUserAssociatedFlags(request):
    response = Response()
    if request.method == 'GET':
        user = request.user
        flag_type = request.GET.get("flag_type", None)
        if flag_type:
            if flag_type == "material" or flag_type == "inspection":
                status_system_code = "system_status_task_status_"+flag_type
                self_task_actions = TaskAction.objects.filter(created_by=user,parent__isnull=True,status__parent__system_code=status_system_code)
                others_task_actions = TaskAction.objects.filter(parent__isnull=True,status__parent__system_code=status_system_code).exclude(created_by=user)

        else:
            self_task_actions = TaskAction.objects.filter(created_by=user,parent__isnull=True)
            others_task_actions = TaskAction.objects.filter(parent__isnull=True).exclude(created_by=user)

        
        total_self_flags = self_task_actions.count()
        total_other_flags = others_task_actions.count()
        
        self_task_action_data = TaskActionSerializer(self_task_actions, many=True).data
        others_task_action_data = TaskActionSerializer(others_task_actions, many=True).data

        # Calculate statistics for self_task_actions
        self_status_counts = calculate_status_counts(self_task_action_data)

        # Calculate statistics for others_task_actions
        others_status_counts = calculate_status_counts(others_task_action_data)

        # Create the response data
        response_data = {
            'success': 1,
            'message': '',
            'response_data': [{"name":"self","total_flags":total_self_flags,"data":self_status_counts},{"name":"others","total_flags":total_other_flags,"data":others_status_counts}],
        }

        response.data = response_data
    else:
        response.data = {'status': 0, 'message': 'Method is not allowed', 'data': None}

    return response


@api_view(['GET','POST'])
@permission_classes([AllowAny])
# @csrf_protect
@csrf_exempt
@authentication_classes([SafeJWTAuthentication, ])
def UpdateProjectProgressView(request):
    response = Response()
    response.data = {'status':0,'message':'Method is not allowed','data':{None}}
    if request.user.is_authenticated:
    	response.data = UpdateProjectProgress(request)
    return response
