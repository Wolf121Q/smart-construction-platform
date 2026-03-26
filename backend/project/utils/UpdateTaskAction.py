from project.models import Task,TaskAction,TaskActionComment,TaskStatus,TaskFile,Project
from core.models import UserProfile
from datetime import datetime,timedelta
from utils.IP import get_client_ip
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import date
from django.http import JsonResponse

def get_quill(value):
    return value
    #return '{"delta":{"ops":[{"insert":"test"}]},"html":"'+value+'"}'

def get_random_task_or_create(request, project_id):
    try:
        # First, check if the project exists
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        error_message = f"Project id is invalid"
        response = {'status': 0, 'message': error_message}
        return response

    # Try to get a random task for the project
    task = Task.objects.filter(project_id=project_id).order_by('?').first()
    # If no task is found, create a new one
    if task is None:
        # Create a new task
        current_date = timezone.now().date()
        # Calculate start date (two years back)
        start_date = current_date - timedelta(days=365 * 2)
        # Calculate end date (one year after)
        end_date = current_date + timedelta(days=365)
        task = Task.objects.create(
            project=project,
            ip=get_client_ip(request),
            created_by=User.objects.filter(is_superuser=True).first(),
            name="Earth Work",
            code=str(project.code)+" "+"Earth Work",
            region=project.region,
            city=project.city,
            organization=project.organization,
            start_date=start_date,
            end_date=end_date,
            latitude=33.630978,
            longitude=73.107480,
        )
        return task
    return task



def UpdateTaskAction(request):
    new_action = "Created"
    # task_id = request.POST.get('task_id',None)
    project_id = request.POST.get('project_id', None)
    task_action_id = request.POST.get('task_action_id', None)
    status_id = request.POST.get('status_id', None)

    description = request.POST.get('description', None)
    # progress_actual = request.POST.get('progress_actual',0)
    latitude = request.POST.get('latitude', 0)
    longitude = request.POST.get('longitude', 0)
    precision = request.POST.get('precision', 0)
    material_name = request.POST.get('material_name', None)
    quantity_type = request.POST.get('quantity_type', None)
    actual_quantity = request.POST.get('actual_quantity', 0)
    damage_quantity = request.POST.get('damage_quantity', 0)
    received_quantity = request.POST.get('received_quantity', 0)
    lab_test_result = request.POST.get('lab_test_result', 3)
    # attachment = request.FILES.get('attachment',None)
    attachments = request.FILES.getlist('attachments', None)

    # Check for user and project zone compatibility
    user_profile = UserProfile.objects.filter(user_id=request.user.id).first()
    task = get_random_task_or_create(request,project_id)
    # task = get_object_or_404(Task, id=task_id)
    project = task.project

    # if user_profile and user_profile.region and user_profile.region != project.region:
    # Region and/or city do not match, return an error JSON response
    # error_message = f"{request.user.username}'s Region and/or city do not match the project's location."
    # response = {'status': 0, 'message': error_message, 'data':{'Project Region: ':project.region.name, 'User\'s Region': user_profile.region.name}}
    # return response

    if description:
        description = get_quill(description)

    # Checking If the flag with same Description, Created By and Task Id exists within last hour
    if not attachments:
        response = {'status': 0, 'message': 'Attachment is required'}
        return response

    # one_hour_ago = datetime.now(tz=ZoneInfo("Asia/Karachi")) - timedelta(hours=1)
    # existing_instances = TaskAction.objects.filter(
    #     created_by=request.user,
    #     description=description,
    #     task_id = task_id,
    #     status_id = status_id,
    # )
    # if existing_instances.first():
    #     response = {'status': 1, 'message': 'Task Action Already Exist'}
    #     return response

    # elif TaskAction.objects.filter(task_id=task_id,status_id=status_id,description=description).count()  > 0:
    #     response = {'status': 2, 'message': 'Task Action Already Exists'}
    #     return response

    response = {'status': 0, 'message': 'Something is Wrong'}
    task_type_inspection = None
    task_type_other = None
    if task is None:
        return {'status': 0, 'message': 'Sorry No Task Found'}

    task_status = TaskStatus.objects.filter(id=status_id).first()
    if task_status is None:
        return {'status': 0, 'message': 'Sorry No Task Status Found'}

    task_action = None
    if task_action_id:
        task_action = TaskAction.objects.filter(id=task_action_id).first()
    else:
        task_action = TaskAction.objects.filter(description=description, created_by=request.user, status=task_status,
                                                created_on__date=date.today()).first()
        if task_action:
            return {'status': 0, 'message': 'Flag already exists'}

    if task_action is None:
        new_task_action = TaskAction()
        new_task_action.task = task
        new_task_action.ip = get_client_ip(request)
        new_task_action.created_by = request.user
        new_task_action.type = task_type_inspection
        new_task_action.project = task.project
        new_task_action.status = task_status
        new_task_action.start_time = datetime.now()
        new_task_action.description = description
        new_task_action.latitude = latitude
        new_task_action.longitude = longitude
        # if precision:
        #     task_action.precision = precision
        new_task_action.save()
        task_action = new_task_action

    else:
        task_action.end_time = datetime.now()
        task_action.duration = (task_action.start_time.astimezone() - task_action.end_time.astimezone())
        task_action.ip = get_client_ip(request)
        task_action.updated_by = request.user
        task_action.save()

        # Creating Children Of TaskAction
        task_action_child = TaskAction()
        task_action_child.task = task
        task_action_child.parent = task_action
        task_action_child.ip = get_client_ip(request)
        task_action_child.created_by = request.user
        task_action_child.type = task_type_inspection
        task_action_child.project = task.project
        task_action_child.status = task_status
        task_action_child.start_time = datetime.now()
        # This is because to store the previous description of the flag
        # task_action_child.description = description
        task_action_child.description = f"{task_action.description} (Rectified)"
        task_action_child.latitude = latitude
        task_action_child.longitude = longitude
        # if precision:
        #     task_action.precision = precision
        task_action_child.save()
        # Updating Task Action
        task_action = task_action_child
        new_action = "Updated"

    if task_action is None:
        return {'status': 0, 'message': 'Sorry No Task Action Found'}

    if description:
        task_action_comment = TaskActionComment()
        task_action_comment.created_by_id = request.user.id
        task_action_comment.ip = get_client_ip(request)
        task_action_comment.status_id = int(status_id)
        task_action_comment.type = task_type_inspection
        task_action_comment.task = task
        task_action_comment.project = task.project
        task_action_comment.task_action = task_action
        task_action_comment.description = description
        task_action_comment.latitude = latitude
        task_action_comment.longitude = longitude
        # if precision:
        #     task_action_comment.precision = precision

        if material_name:
            task_action_comment.material_name = str(material_name)
            task_action_comment.quantity_type = str(quantity_type)
            task_action_comment.actual_quantity = float(actual_quantity)
            task_action_comment.damage_quantity = float(damage_quantity)
            task_action_comment.received_quantity = float(received_quantity)
            task_action_comment.lab_test_result = lab_test_result

        # if task_status.system_code in ['system_status_task_status_material_red','system_status_task_status_inspection_red']:
        #     task_action_comment.is_acknowledged = False
        #     # Creating a notification regarding red flag
        #     try:
        #         if request.user:
        #             sender = User.objects.get(id=request.user.id)
        #             notify.send(sender,action_object= task_action_comment, verb='Message', description=description)
        #     except Exception as e:
        #         TracebackEmail()
        #         return HttpResponse("Please login from admin site for sending messages")

        task_action_comment.save()

    if attachments:
        for attachment in attachments:
            task_attachment = TaskFile()
            task_attachment.created_by_id = request.user.id
            task_attachment.ip = get_client_ip(request)
            task_attachment.status_id = status_id
            task_attachment.type = task_type_inspection
            task_attachment.task = task
            task_attachment.organization = task.project.organization
            task_attachment.project = task.project
            task_attachment.task_action = task_action
            task_attachment.latitude = latitude
            task_attachment.longitude = longitude
            # if precision:
            #     task_attachment.precision = precision
            task_attachment.attachment = attachment
            task_attachment.task_action_comment = task_action_comment
            task_attachment.save()

        action_name = str(task_status.parent.name)
        action_flag_name = str(task_status.name)

    return {'status': 1,
            'message': str(action_name) + ' Flag (' + action_flag_name + ') ' + str(new_action) + ' successfully'}


# def UpdateTaskAction(request):
#     new_action = "Created"
#     task_id = request.POST.get('task_id',None)
#     task_action_id = request.POST.get('task_action_id',None)
#     status_id = request.POST.get('status_id',None)

#     description = request.POST.get('description',None)
#     #progress_actual = request.POST.get('progress_actual',0)
#     latitude = request.POST.get('latitude',0)
#     longitude = request.POST.get('longitude',0)
#     precision = request.POST.get('precision',0)
#     material_name = request.POST.get('material_name',None)
#     quantity_type = request.POST.get('quantity_type',None)
#     actual_quantity = request.POST.get('actual_quantity',0)
#     damage_quantity = request.POST.get('damage_quantity',0)
#     received_quantity = request.POST.get('received_quantity',0)
#     #attachment = request.FILES.get('attachment',None)
#     attachments = request.FILES.getlist('attachments',None)


#     # Check for user and project zone compatibility
#     user_profile = UserProfile.objects.filter(user_id=request.user.id).first()
#     task = get_object_or_404(Task, id=task_id)
#     project = task.project
    
#     if user_profile and user_profile.region != project.region:
#         # Region and/or city do not match, return an error JSON response
#         error_message = f"{request.user.username}'s Region and/or city do not match the project's location."
#         return JsonResponse({'status': 0, 'message': error_message}, status=400)
    
#     if description:
#         description = get_quill(description)

#     # Checking If the flag with same Description, Created By and Task Id exists within last hour
#     if not attachments:
#         response = {'status': 0, 'message': 'Task Action Already Exist'}
#         return response
   
    
#     # one_hour_ago = datetime.now(tz=ZoneInfo("Asia/Karachi")) - timedelta(hours=1)
#     # existing_instances = TaskAction.objects.filter(
#     #     created_by=request.user, 
#     #     description=description,
#     #     task_id = task_id,
#     #     status_id = status_id,
#     # )
#     # if existing_instances.first():
#     #     response = {'status': 1, 'message': 'Task Action Already Exist'}
#     #     return response
    
#     # elif TaskAction.objects.filter(task_id=task_id,status_id=status_id,description=description).count()  > 0:
#     #     response = {'status': 2, 'message': 'Task Action Already Exists'}
#     #     return response

#     response = {'status':0,'message':'Something is Wrong'}
#     task_type_inspection = None
#     task_type_other = None
#     task = Task.objects.filter(id=task_id).first()
#     if task is None:
#         return {'status':0,'message':'Sorry No Task Found'}

#     task_status = TaskStatus.objects.filter(id=status_id).first()
#     if task_status is None:
#         return {'status': 0, 'message': 'Sorry No Task Status Found'}

#     task_action = None
#     if task_action_id:
#         task_action = TaskAction.objects.filter(id=task_action_id).first()
#     else:
#         task_action = TaskAction.objects.filter(description=description,created_by=request.user,status= task_status,created_on__date=date.today()).first()
#         if task_action:
#             return {'status':0,'message':'Flag already exists'}
    
#     if task_action is None:
#         new_task_action = TaskAction()
#         new_task_action.task_id = task_id
#         new_task_action.ip = get_client_ip(request)
#         new_task_action.created_by = request.user
#         new_task_action.type = task_type_inspection
#         new_task_action.project = task.project
#         new_task_action.status = task_status
#         new_task_action.start_time = datetime.now()
#         new_task_action.description = description
#         new_task_action.latitude = latitude
#         new_task_action.longitude = longitude
#         # if precision:
#         #     task_action.precision = precision
#         new_task_action.save()
#         task_action = new_task_action

#     else:
#         task_action.end_time = datetime.now()
#         task_action.duration = (task_action.start_time.astimezone() - task_action.end_time.astimezone())
#         task_action.ip = get_client_ip(request)
#         task_action.updated_by = request.user
#         task_action.save()

#         # Creating Children Of TaskAction
#         task_action_child = TaskAction()
#         task_action_child.task_id = task_id
#         task_action_child.parent = task_action
#         task_action_child.ip = get_client_ip(request)
#         task_action_child.created_by = request.user
#         task_action_child.type = task_type_inspection
#         task_action_child.project = task.project
#         task_action_child.status = task_status
#         task_action_child.start_time = datetime.now()
#         # This is because to store the previous description of the flag
#         #task_action_child.description = description
#         task_action_child.description = f"{task_action.description} (Rectified)"
#         task_action_child.latitude = latitude
#         task_action_child.longitude = longitude
#         # if precision:
#         #     task_action.precision = precision
#         task_action_child.save()
#         # Updating Task Action
#         task_action = task_action_child
#         new_action = "Updated"

#     if task_action is None:
#         return {'status': 0, 'message': 'Sorry No Task Action Found'}

#     if description:
#         task_action_comment = TaskActionComment()
#         task_action_comment.created_by_id = request.user.id
#         task_action_comment.ip = get_client_ip(request)
#         task_action_comment.status_id = int(status_id)
#         task_action_comment.type = task_type_inspection
#         task_action_comment.task = task
#         task_action_comment.project = task.project
#         task_action_comment.task_action = task_action
#         task_action_comment.description = description
#         task_action_comment.latitude = latitude
#         task_action_comment.longitude = longitude
#         # if precision:
#         #     task_action_comment.precision = precision
        
#         if material_name:
#             task_action_comment.material_name = str(material_name)
#             task_action_comment.quantity_type = str(quantity_type)
#             task_action_comment.actual_quantity = float(actual_quantity)
#             task_action_comment.damage_quantity = float(damage_quantity)
#             task_action_comment.received_quantity = float(received_quantity)

#         # if task_status.system_code in ['system_status_task_status_material_red','system_status_task_status_inspection_red']:
#         #     task_action_comment.is_acknowledged = False
#         #     # Creating a notification regarding red flag 
#         #     try:
#         #         if request.user:
#         #             sender = User.objects.get(id=request.user.id)
#         #             notify.send(sender,action_object= task_action_comment, verb='Message', description=description)
#         #     except Exception as e:
#         #         TracebackEmail()
#         #         return HttpResponse("Please login from admin site for sending messages")

#         task_action_comment.save()

#     if attachments:
#         for attachment in attachments:
#             task_attachment = TaskFile()
#             task_attachment.created_by_id = request.user.id
#             task_attachment.ip = get_client_ip(request)
#             task_attachment.status_id = status_id
#             task_attachment.type = task_type_inspection
#             task_attachment.task = task
#             task_attachment.organization = task.project.organization
#             task_attachment.project = task.project
#             task_attachment.task_action = task_action
#             task_attachment.latitude = latitude
#             task_attachment.longitude = longitude
#             # if precision:
#             #     task_attachment.precision = precision
#             task_attachment.attachment = attachment
#             task_attachment.task_action_comment = task_action_comment
#             task_attachment.save()

#         action_name = str(task_status.parent.name)
#         action_flag_name = str(task_status.name)

#     return {'status':1,'message':str(action_name)+' Flag ('+action_flag_name+') '+ str(new_action)+' successfully'}


        
def UpdateTasksProgress(request):
    task_id = request.POST.get('task_id',None)
    description = request.POST.get('description',None)
    progress_actual = request.POST.get('progress_actual',0)
    latitude = request.POST.get('latitude',0)
    longitude = request.POST.get('longitude',0)
    precision = request.POST.get('precision',0)
    start_date = request.POST.get('start_date',None)
    end_date = request.POST.get('end_date',None)
    task = None
    if description:
        description = get_quill(description)
    if task_id:
        task = Task.objects.filter(id=task_id).first()
    if task is None:
        return {'status':0,'message':'Sorry No Task Found'}
    else:
        task.ip = get_client_ip(request)
        task.updated_by = request.user
        task.latitude = latitude
        task.longitude = longitude
        task.precision = precision
        task.description = description
        task.progress_actual = progress_actual
        task.start_date = start_date
        task.end_date = end_date
        task.save()

        # Updating Project Progress Based On Individual Task Progress Update
        # Resetting Project's Progress
        project = task.project
        project.progress_actual = Decimal(0)
        project.save()
        
        tasks = project.project_task_related.all()
        if tasks.count() == 0:
            return 0
        total_progress = sum(task.progress_actual for task in tasks)
        project_progress = total_progress / (tasks.count() * 100) * 100
        project.progress_actual = project_progress
        project.save()

        return {'status': 1,'message':'Task '+str(task.name) + ' progress updated successfully'}

def UpdateProjectProgress(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id', None)
        description = request.POST.get('description', None)
        progress_actual = request.POST.get('progress_actual', None)
        progress_planned = request.POST.get('progress_planned', 0)
        if description:
            description = get_quill(description)
        if progress_actual is None:
            return {'status': 0, 'message': 'Progress Actual is required'}
        if project_id:
            project = Project.objects.filter(id=project_id).first()
            if project is None:
                # return {'status':0,'message':'Sorry No Task Found'}
                return {'status': 0, 'message': 'Sorry No Project Found', 'data': {'project_id': project_id}}
            else:
                project.updated_by = request.user
                project.progress_actual = progress_actual
                project.progress_planned = progress_planned
                project.save()
                return {'status': 1,
                        'message': 'Project ' + str(project.project_label) + ' progress updated successfully'}

    elif request.method == 'GET':
        project_id = request.GET.get('project_id', None)
        if project_id:
            project = Project.objects.filter(id=project_id).first()
            if project is None:
                return {'status': 0, 'message': 'Sorry No Project Found', 'data': {'project_id': project_id}}
            return {'status': 1,
                    'data': {'progress_actual': project.progress_actual, 'progress_planned': project.progress_planned}}

