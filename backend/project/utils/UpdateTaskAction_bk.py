from project.models import Task,TaskAction,TaskActionComment,TaskStatus,TaskFile
from datetime import datetime
from core.submodels.SystemStatus import SystemStatus
from utils.IP import get_client_ip
from django.utils.safestring import mark_safe
from django.contrib import messages
from django_quill.quill import Quill

def get_quill(value):
    return '{"delta":{"ops":[{"insert":"test"}]},"html":"'+value+'"}'

def UpdateTaskAction(request):
    
    task_id = request.POST.get('task_id',None)
    status_id = request.POST.get('status_id',None)
    description = request.POST.get('description',None)
    progress_actual = request.POST.get('progress_actual',0)
    latitude = request.POST.get('latitude',0)
    longitude = request.POST.get('longitude',0)
    precision = request.POST.get('precision',0)
    task_action_id = request.POST.get('task_action_id',None)
    material_name = request.POST.get('material_name',None)
    quantity_type = request.POST.get('quantity_type',None)
    actual_quantity = request.POST.get('actual_quantity',0)
    damage_quantity = request.POST.get('damage_quantity',0)
    received_quantity = request.POST.get('received_quantity',0)
    #attachment = request.FILES.get('attachment',None)
    attachments = request.FILES.getlist('attachments',None)
    if description:
        description = get_quill(description)

    response = {'status':0,'message':'Something is Wrong'}
    task_type_inspection = None
    task_type_other = None
    task = Task.objects.filter(id=task_id).first()
    task_status = TaskStatus.objects.filter(id=status_id).first()

    task_action = None

    if task_status:
        if task_status.parent.system_code == "system_status_task_status_inspection":
            task_type_inspection = task_status.parent
            if task_status.system_code == "system_status_task_status_inspection_completed":
                if TaskAction.objects.filter(task_id=task_id,end_time__isnull=True).count() == 0:
                    return  {'status':0,'message':'Wrong Action Status'}
                elif TaskAction.objects.filter(task_id=task_id,end_time__isnull=True).exclude(type=task_type_inspection).count() > 0:
                    return {'status': 0, 'message': 'Others Flag Still Open'}
        else:
            task_type_other = task_status.parent

    if task_type_inspection:
        task_action = TaskAction.objects.filter(type=task_type_inspection,task_id=task_id,end_time__isnull=True).first()

        if task_action is not None:
            if int(task_action.status_id) != int(status_id):
                task_action.end_time = datetime.now()
                task_action.duration = (task_action.start_time.astimezone() - task_action.end_time.astimezone())
                task_action.ip = get_client_ip(request)
                task_action.updated_by = request.user
                task_action.end_progress = progress_actual
                task_action.save()

                task_action = TaskAction()
                task_action.task_id = task_id
                task_action.ip = get_client_ip(request)
                task_action.created_by = request.user
                task_action.type = task_type_inspection
                task_action.project = task.project
                task_action.status = task_status
                task_action.start_time = datetime.now()
                task_action.description = description
                task_action.start_progress = progress_actual
                task_action.latitude = latitude
                task_action.longitude = longitude
                task_action.precision = precision
                task_action.save()
            else:
                #task_action.end_time = datetime.now()
                task_action.duration = (task_action.start_time.astimezone() - datetime.now().astimezone())
                task_action.ip = get_client_ip(request)
                task_action.updated_by = request.user
                task_action.end_progress = progress_actual
                task_action.save()

            if description:
                task_action_comment = TaskActionComment()
                task_action_comment.created_by_id = request.user.id
                task_action_comment.ip = get_client_ip(request)
                task_action_comment.status_id = status_id
                task_action_comment.type = task_type_inspection
                task_action_comment.task = task
                task_action_comment.project = task.project
                task_action_comment.task_action = task_action
                task_action_comment.description = description
                task_action_comment.progress_actual = progress_actual
                task_action_comment.latitude = latitude
                task_action_comment.longitude = longitude
                task_action_comment.precision = precision
                task_action_comment.material_name = material_name
                task_action_comment.quantity_type = quantity_type
                task_action_comment.actual_quantity = actual_quantity
                task_action_comment.damage_quantity = damage_quantity
                task_action_comment.received_quantity = received_quantity
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
                    task_attachment.progress_actual = progress_actual
                    task_attachment.latitude = latitude
                    task_attachment.longitude = longitude
                    task_attachment.precision = precision
                    task_attachment.attachment = attachment
                    task_attachment.task_action_comment = task_action_comment
                    task_attachment.save()


        elif TaskAction.objects.filter(type=task_type_inspection,task_id=task_id).count() == 0:

                task_action = TaskAction()
                task_action.task_id = task_id
                task_action.ip = get_client_ip(request)
                task_action.created_by = request.user
                task_action.type = task_type_inspection
                task_action.project = task.project
                task_action.status = task_status
                task_action.start_time = datetime.now()
                task_action.description = description
                task_action.start_progress = progress_actual
                task_action.latitude = latitude
                task_action.longitude = longitude
                task_action.precision = precision
                task_action.save()

                if description:
                    task_action_comment = TaskActionComment()
                    task_action_comment.created_by_id = request.user.id
                    task_action_comment.ip = get_client_ip(request)
                    task_action_comment.status_id = status_id
                    task_action_comment.type = task_type_inspection
                    task_action_comment.task = task
                    task_action_comment.project = task.project
                    task_action_comment.task_action = task_action
                    task_action_comment.description = description
                    task_action_comment.progress_actual = progress_actual
                    task_action_comment.latitude = latitude
                    task_action_comment.longitude = longitude
                    task_action_comment.precision = precision
                    task_action_comment.material_name = material_name
                    task_action_comment.quantity_type = quantity_type
                    task_action_comment.actual_quantity = actual_quantity
                    task_action_comment.damage_quantity = damage_quantity
                    task_action_comment.received_quantity = received_quantity
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
                        task_attachment.progress_actual = progress_actual
                        task_attachment.latitude = latitude
                        task_attachment.longitude = longitude
                        task_attachment.precision = precision
                        task_attachment.attachment = attachment
                        task_attachment.task_action_comment = task_action_comment
                        task_attachment.save()


        task.updated_by = request.user
        task.ip = get_client_ip(request)
        task.progress_actual = progress_actual
        task.status_id = status_id
        task.save()

        return {'status':1,'message':'Task Inspection Updated'}

    elif task_type_other:
        if task_action_id:
            task_action = TaskAction.objects.filter(id=task_action_id,type=task_type_other, task_id=task_id,end_time__isnull=True).first()

            if task_action is not None:
                if int(task_action.status_id) != int(status_id):
                    task_action.end_time = datetime.now()
                    task_action.duration = (task_action.start_time.astimezone() - task_action.end_time.astimezone())
                    task_action.ip = get_client_ip(request)
                    task_action.updated_by = request.user
                    task_action.save()

                    task_action = TaskAction()
                    task_action.task_id = task_id
                    task_action.ip = get_client_ip(request)
                    task_action.created_by = request.user
                    task_action.type = task_type_other
                    task_action.project = task.project
                    task_action.status = task_status
                    task_action.start_time = datetime.now()
                    task_action.description = description
                    task_action.latitude = latitude
                    task_action.longitude = longitude
                    task_action.precision = precision
                    task_action.save()

                if description:
                    task_action_comment = TaskActionComment()
                    task_action_comment.created_by_id = request.user.id
                    task_action_comment.ip = get_client_ip(request)
                    task_action_comment.status_id = status_id
                    task_action_comment.type = task_type_other
                    task_action_comment.task = task
                    task_action_comment.project = task.project
                    task_action_comment.task_action = task_action
                    task_action_comment.description = description
                    task_action_comment.progress_actual = progress_actual
                    task_action_comment.latitude = latitude
                    task_action_comment.longitude = longitude
                    task_action_comment.precision = precision
                    task_action_comment.material_name = material_name
                    task_action_comment.quantity_type = quantity_type
                    task_action_comment.actual_quantity = actual_quantity
                    task_action_comment.damage_quantity = damage_quantity
                    task_action_comment.received_quantity = received_quantity
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
                        task_attachment.progress_actual = progress_actual
                        task_attachment.latitude = latitude
                        task_attachment.longitude = longitude
                        task_attachment.precision = precision
                        task_attachment.attachment = attachment
                        task_attachment.task_action_comment = task_action_comment
                        task_attachment.save()

                return {'status': 1, 'message': 'Task '+str(task_type_other.name)+' Updated'}

            else:
                task_action = TaskAction()
                task_action.task_id = task_id
                task_action.ip = get_client_ip(request)
                task_action.created_by = request.user
                task_action.type = task_type_inspection
                task_action.project = task.project
                task_action.status = task_status
                task_action.start_time = datetime.now()
                task_action.description = description
                task_action.start_progress = progress_actual
                task_action.latitude = latitude
                task_action.longitude = longitude
                task_action.precision = precision
                task_action.save()
                if description:
                    task_action_comment = TaskActionComment()
                    task_action_comment.created_by_id = request.user.id
                    task_action_comment.ip = get_client_ip(request)
                    task_action_comment.status_id = status_id
                    task_action_comment.task = task
                    task_action_comment.project = task.project
                    task_action_comment.task_action = task_action
                    task_action_comment.description = description
                    task_action_comment.progress_actual = progress_actual
                    task_action_comment.latitude = latitude
                    task_action_comment.longitude = longitude
                    task_action_comment.precision = precision
                    task_action_comment.material_name = material_name
                    task_action_comment.quantity_type = quantity_type
                    task_action_comment.actual_quantity = actual_quantity
                    task_action_comment.damage_quantity = damage_quantity
                    task_action_comment.received_quantity = received_quantity
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
                        task_attachment.progress_actual = progress_actual
                        task_attachment.latitude = latitude
                        task_attachment.longitude = longitude
                        task_attachment.precision = precision
                        task_attachment.attachment = attachment
                        task_attachment.task_action_comment = task_action_comment
                        task_attachment.save()

            return {'status': 1, 'message': 'Task ' + str(task_type_other.name) + ' Updated'}
        
        elif TaskAction.objects.filter(type=task_type_other,task_id=task_id).count() == 0:
            task_action = TaskAction()
            task_action.task_id = task_id
            task_action.ip = get_client_ip(request)
            task_action.created_by = request.user
            task_action.type = task_type_inspection
            task_action.project = task.project
            task_action.status = task_status
            task_action.start_time = datetime.now()
            task_action.description = description
            task_action.start_progress = progress_actual
            task_action.latitude = latitude
            task_action.longitude = longitude
            task_action.precision = precision
            task_action.save()

            if description:
                task_action_comment = TaskActionComment()
                task_action_comment.created_by_id = request.user.id
                task_action_comment.ip = get_client_ip(request)
                task_action_comment.status_id = status_id
                task_action_comment.type = task_type_inspection
                task_action_comment.task = task
                task_action_comment.project = task.project
                task_action_comment.task_action = task_action
                task_action_comment.description = description
                task_action_comment.progress_actual = progress_actual
                task_action_comment.latitude = latitude
                task_action_comment.longitude = longitude
                task_action_comment.precision = precision
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
                    task_attachment.progress_actual = progress_actual
                    task_attachment.latitude = latitude
                    task_attachment.longitude = longitude
                    task_attachment.precision = precision
                    task_attachment.attachment = attachment
                    task_attachment.task_action_comment = task_action_comment
                    task_attachment.save()
        
        task.updated_by = request.user
        task.ip = get_client_ip(request)
        task.progress_actual = progress_actual
        task.status_id = status_id
        task.save()

        return {'status':1,'message':'Task Material Added Successfully'}

