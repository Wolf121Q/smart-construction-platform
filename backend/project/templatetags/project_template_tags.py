from multiprocessing import reduction
from pstats import Stats
from django import template
from app_admin.templatetags.bootstrap_admin_template_tags import widget_type
from project.models import Task,TaskActionTimeLine
from project.models import Project,TaskAction,TaskActionComment,TaskFile
from django.utils.safestring import mark_safe
from django.db.models import Subquery
from organization.models import Region
from core.models import SystemStatus
from project.utils.TaskActionTimeLine import CalculateTaskActionTimeLineRaised,CalculateTaskActionTimeLineCleared,CalculateTaskActionTimeLineBalance
# Depending on your django version, `reverse` and `NoReverseMatch` has been moved.
# From django 2.0 they've been moved to `django.urls`
try:
    from django.urls import reverse, NoReverseMatch
except ImportError:
    from django.core.urlresolvers import reverse, NoReverseMatch

register = template.Library()

# From django 1.9 `assignment_tag` is deprecated in favour of `simple_tag`
try:
    simple_tag = register.simple_tag
except AttributeError:
    simple_tag = register.assignment_tag


# CS
@register.filter()
def flag_status_count(status_id,request):
    flag_status_count = TaskAction.objects.filter(status_id =status_id,end_time__isnull = True).count()
    if flag_status_count:
        return flag_status_count
    else:
        return 0


@register.filter()
def project_flag_status_count(status_id,project_id):
    completed_project_count = TaskAction.objects.filter(status_id =status_id,project_id=project_id).count()
    if completed_project_count:
        return completed_project_count
    else:
        return 0

@register.filter()
def get_task_actions(task,request):
    task_actions = TaskAction.objects.filter(task_id =task.id)
    if task_actions:
        return task_actions
    else:
        return {}

@register.filter()
def get_task_remarks(task_action,request):
    task_actions = TaskActionComment.objects.filter(task_action_id =task_action.id)
    if task_actions:
        return task_actions
    else:
        return {}

@register.filter()
def get_task_remarks_files(task_action_comment,request):
    if task_action_comment:
        task_actions = TaskFile.objects.filter(task_action_comment_id =task_action_comment.id)
        if task_actions:
            return task_actions
    else:
        return {}


@register.filter()
def flag_per_project(project_id):
    task_count = Task.objects.filter(project_id = project_id).values('status').count()
    if task_count:
        return task_count
    else:
        return ""


@register.filter()
def project_count_citywise_inprogress(city_id,user):
    valid_project_count = Project.objects.filter(organization__region__users = user,city_id = city_id,status__system_code = 'system_status_project_status_valid').count()
    if valid_project_count:
        return valid_project_count
    else:
        return 0

@register.filter()
def project_count_citywise_completed(city_id,user):
    completed_project_count = Project.objects.filter(organization__region__users = user,city_id = city_id,status__system_code = 'system_status_project_status_completed').count()
    if completed_project_count:
        return completed_project_count
    else:
        return 0
    
@simple_tag
def project_count_regionwise(region,qs):
    if region:
        return qs.filter(region_id = region.id).count()
    else:
        return 0


@simple_tag
def task_action_inspection_count(task_id,project_id):
    inspection_count = TaskAction.objects.filter(task_id = task_id, project_id = project_id,status__parent__system_code = 'system_status_task_status_inspection').count()
    if inspection_count:
        return inspection_count
    else:
        return 0
@simple_tag
def task_action_material_count(task_id,project_id):
    material_count = TaskAction.objects.filter(task_id = task_id, project_id = project_id,status__parent__system_code = 'system_status_task_status_material').count()
    if material_count:
        return material_count
    else:
        return 0

@simple_tag
def task_action_attachment(task_id,task_action_id):
    task_file_qs = TaskFile.objects.filter(task_id = task_id, task_action_id = task_action_id)
    if task_file_qs:
        for file in task_file_qs:
            return mark_safe('<li><img class="rounded" src="{url}" width = {width} height = {height}/></li>'.format(
                url=file.attachment.url,
                width = '80px',
                height = '80px',
            ))
    else:
        return ""
    
@simple_tag
def task_action_comment_attachment(task_id,task_action_comment_id):
    ta_attachment = TaskFile.objects.filter(task_id = task_id, task_action_comment_id = task_action_comment_id).first()
    if ta_attachment:
        task_action_comment_attachment_url = ta_attachment.attachment.url
        if task_action_comment_attachment_url:
            return mark_safe('<img src="{url}" width={width} height = {height}/>'.format(
                url=task_action_comment_attachment_url,
                width = "50px",
                height = "50px",
            ))
        else:
            return ""
    return ""

@simple_tag
def getTaskActionComment(task_action_id,id="",created_by = "",created_on = ""):
    task_action_comment_obj = TaskActionComment.objects.filter(task_action_id = task_action_id).first()
    if task_action_comment_obj:
        if id == True:
            return task_action_comment_obj.id
        elif created_by == True:
            return task_action_comment_obj.created_by
        elif created_on == True:
            return task_action_comment_obj.created_on.strftime("%m/%d/%Y, %H:%M:%S")
        else:
            return mark_safe(task_action_comment_obj.description) 
    else:
        return ""



""" CAN BE REMOVED """
@simple_tag
def getCommentFromAction(task_action_id):
    task_action_comment_obj = TaskActionComment.objects.filter(task_action_id = task_action_id).first()
    if task_action_comment_obj:
        return task_action_comment_obj.id
    else:
        return TaskActionComment.objects.none()

@simple_tag
def subtract(value, arg):
    if value and arg:
        return value - arg
    else:
        return 0.0

@register.filter()
def action_comment_reply(task_action_comment_id):
    task_action_comment_qs = TaskActionComment.objects.filter(parent_id = task_action_comment_id,reply=True).order_by('-created_on')
    if task_action_comment_qs:
        return task_action_comment_qs
    else:
        return TaskActionComment.objects.none()


@register.filter()
def getInboxComments(request):
    tagged_comments = TaskActionComment.objects.filter(tag_to_id = request.user.id).order_by("-created_on")
    if tagged_comments:
        return tagged_comments
    else:
        return TaskActionComment.objects.none()
   
@simple_tag
def inbox_comments(task_id,task_action_comment_id):
    task_action_comment = TaskActionComment.objects.filter(task_id = task_id, id = task_action_comment_id).first()
    if task_action_comment:
        if task_action_comment.tag_to.avatar:
            return mark_safe('<a href="#{serial_number}" class="list-group-item list-group-item-action border-bottom">\
                            <div class="row align-items-center"><div class="col-auto"> <img alt="Image placeholder" src="{profile_pic}" class="avatar-md rounded"></div>\
                            <div class="col ps-0 ms-2"><div class="d-flex justify-content-between align-items-center"><div>\
                            <h4 class="h6 mb-0 text-small">{tag_to}</h4></div><div class="text-end mx-5"><small class="text-danger">{tag_time}</small></div></div>\
                            <p class="font-small mt-1 mb-0">{comment}</p>\
                            </div></div></a>'.format(serial_number = task_action_comment.serial_number,profile_pic=task_action_comment.tag_to.avatar.url,tag_to = task_action_comment.tag_to.full_name,comment = task_action_comment.description,tag_time=task_action_comment.tag_time.strftime("%m-%d-%Y, %H:%M:%S")))
    else:
        return mark_safe('<a href="#{serial_number}" class="list-group-item list-group-item-action border-bottom">\
                <div class="row align-items-center"><div class="col-auto"> <img alt="Image placeholder" class="avatar-md rounded"></div>\
                <div class="col ps-0 ms-2"><div class="d-flex justify-content-between align-items-center"><div>\
                <h4 class="h6 mb-0 text-small">{tag_to}</h4></div><div class="text-end mx-5"><small class="text-danger">{tag_time}</small></div></div>\
                <p class="font-small mt-1 mb-0">{comment}</p>\
                </div></div></a>'.format(serial_number = task_action_comment.serial_number,tag_to = task_action_comment.tag_to.full_name,comment = task_action_comment.description,tag_time=task_action_comment.tag_time.strftime("%m-%d-%Y, %H:%M:%S")))



# FLAGS PER TASK
@register.filter()
def inspection_flag_per_task(task):
    inpection_flag_count = TaskAction.objects.filter(task_id = task.id,status__parent__system_code = 'system_status_task_status_inspection').count()
    if inpection_flag_count:
        return inpection_flag_count
    else:
        return 0

@register.filter()
def material_flag_per_task(task):
    material_flag_per_task = TaskAction.objects.filter(task_id = task.id,status__parent__system_code = 'system_status_task_status_material').count()
    if material_flag_per_task:
        return material_flag_per_task
    else:
        return 0

# TASK RELATED TAGS ON CHANGE LIST PAGE

@simple_tag
def project_count_citywise(city,qs):
    project_count = qs.filter(city_id = city.id).count()
    if project_count:
        return project_count
    else:
        return 0


@simple_tag
def tagged_to_task_action(task_action_id):
    task_action_comment = TaskActionComment.objects.filter(task_action_id = task_action_id).first()
    if task_action_comment and task_action_comment.tag_to:
        return mark_safe("<small>{user}:{tag_time}".format(user=task_action_comment.tag_to.full_name,tag_time=task_action_comment.tag_time))
    else:
        return " "

@simple_tag
def task_action_remarks_source(task_action_id):
    task_action_comment = TaskActionComment.objects.filter(task_action_id = task_action_id).first()
    if task_action_comment and task_action_comment.created_by:
        return task_action_comment.created_by.full_name
    else:
        return ""

# ATTRIBUTES OF COMMENT
@register.filter
def get_action_comment_id(obj):
    task_action_comment1 = TaskActionComment.objects.filter(task_action_id = obj.id,reply=False).first()
    if task_action_comment1:
        return task_action_comment1.id
    else:
        return ""

@register.filter
def get_action_comment_desc(obj):
    task_action_comment1 = TaskActionComment.objects.filter(task_action_id = obj.id,reply=False).first()
    if task_action_comment1:
        return task_action_comment1.description
    else:
        return ""

@register.filter
def get_action_comment_created_by(obj):
    task_action_comment1 = TaskActionComment.objects.filter(task_action_id = obj.id,reply=False).first()
    if task_action_comment1:
        return task_action_comment1.created_by
    else:
        return ""

@register.filter
def get_action_comment_created_on(obj):
    task_action_comment1 = TaskActionComment.objects.filter(task_action_id = obj.id,reply=False).first()
    if task_action_comment1:
        return task_action_comment1.created_on
    else:
        return ""
   
@simple_tag
def total_flags_count(category):
    cat_name = str(category.name).lower()
    total_flags = TaskAction.objects.filter(status__system_code__icontains = cat_name,end_time__isnull = True).count()
    return total_flags


@simple_tag
def total_flags_count(category):
    cat_name = str(category.name).lower()
    total_flags = TaskAction.objects.filter(status__system_code__icontains = cat_name,end_time__isnull = True).count()
    return total_flags

@register.filter
def check_if_attachment_exists(task_action_comment_id):
    task_files = TaskFile.objects.filter(task_action_comment_id = task_action_comment_id).count()
    if task_files:
        return True
    else:
        return False

@register.filter
def check_for_first_attachment(task_action_id):
    task_action_comment = TaskActionComment.objects.filter(task_action_id = task_action_id,parent__isnull = True).first()
    if task_action_comment:
        task_files = TaskFile.objects.filter(task_action_comment = task_action_comment.id).count()
        if task_files:
            return True
        else:
            return False
    else:
        return False         

@simple_tag
def raised_flags_status_count(status,qs,request=None):
    if status.system_code in ['system_status_task_status_material_green','system_status_task_status_inspection_green']:
        return 0
    
    if request is not None:
        flag_id = request.GET.get('flag_id',None)
        if flag_id is not None and int(flag_id) != int(status.id):
            return 0

        time_line = TaskActionTimeLine.objects.filter(user_type_id = request.user.type.id).first()
        if time_line:
            flag_type = time_line.flag_type 
            status_type = SystemStatus.objects.filter(id = status.id).first().type
            if status_type == flag_type:
                total_flags = CalculateTaskActionTimeLineRaised(status,qs,time_line)
                return total_flags

            else:
                total_flags = TaskAction.objects.filter(project_id__in = Subquery(qs.values('id')),status_id=status.id).count()
                return total_flags
    
        else:
            total_flags = TaskAction.objects.filter(project_id__in = Subquery(qs.values('id')),status_id=status.id).count()
            return total_flags

    else:
        total_flags = TaskAction.objects.filter(project_id__in = Subquery(qs.values('id')),status_id=status.id).count()
        return total_flags
    

@simple_tag
def cleared_flags_status_count(status,qs,request=None):
    cleared_flag_green_sys_code = str(status.parent.system_code)+"_green"
    if status.system_code in ['system_status_task_status_material_green','system_status_task_status_inspection_green']:
        return 0
    
    if request is not None:
        flag_id = request.GET.get('flag_id',None)
        if flag_id is not None and int(flag_id) != int(status.id):
            return 0

        time_line = TaskActionTimeLine.objects.filter(user_type_id = request.user.type.id).first()
        if time_line:
            flag_type = time_line.flag_type 
            status_type = SystemStatus.objects.filter(id = status.id).first().type
            if status_type == flag_type:
                total_flags = CalculateTaskActionTimeLineCleared(status,qs,time_line)
                return total_flags
            else:
                total_flags = TaskAction.objects.filter(project_id__in = Subquery(qs.values('id')),status_id=status.id,end_time__isnull = False).count()
                return total_flags

        else:
            total_flags = TaskAction.objects.filter(project_id__in = Subquery(qs.values('id')),status_id=status.id,end_time__isnull = False).count()
            return total_flags
    else:
        total_flags = TaskAction.objects.filter(project_id__in = Subquery(qs.values('id')),status_id=status.id,end_time__isnull = False).count()
        return total_flags

@simple_tag
def balance_flags_status_count(status,qs,request=None):
    # if status.system_code in ['system_status_task_status_material_green','system_status_task_status_inspection_green']:
    #     return TaskAction.objects.filter(project_id__in = Subquery(qs.values('id')),status_id=status.id,end_time__isnull = True).count()
   
    if request is not None:
        flag_id = request.GET.get('flag_id',None)
        if flag_id is not None and int(flag_id) != int(status.id):
            return 0
        
        time_line = TaskActionTimeLine.objects.filter(user_type_id = request.user.type.id).first()
        if time_line:
            flag_type = time_line.flag_type 
            status_type = SystemStatus.objects.filter(id = status.id).first().type
            if status_type == flag_type:
                total_flags = CalculateTaskActionTimeLineBalance(status,qs,time_line)
                return total_flags
            else:
                total_flags = TaskAction.objects.filter(project_id__in = Subquery(qs.values('id')),status_id=status.id,end_time__isnull = True).count()
                return total_flags

        else:
            total_flags = TaskAction.objects.filter(project_id__in = Subquery(qs.values('id')),status_id=status.id,end_time__isnull = True).count()
            return total_flags
    else:
        total_flags = TaskAction.objects.filter(project_id__in = Subquery(qs.values('id')),status_id=status.id,end_time__isnull = True).count()
        return total_flags
    
    
    # if request is not None:
    #     total_flags = int(raised_flags_status_count(status,qs,request)) - int(cleared_flags_status_count(status,qs,request))
    #     if total_flags >=0:
    #         return total_flags
    #     else:
    #         return 0
    # else:
    #     total_flags = int(raised_flags_status_count(status,qs)) - int(cleared_flags_status_count(status,qs))
    #     return total_flags


@simple_tag
def flag_type_status_count(status_type,qs):
    total_flags = TaskAction.objects.filter(project_id__in = Subquery(qs.values('id')),status__type__id=status_type.id,end_time__isnull = True).count()
    return total_flags
    
# TOTAL OF MATERIAL AND INSPECTION FLAG IN FLAG CARD
@simple_tag
def total_inspection_flag_raised_status_count(flag_type,qs,request=None):
    project_ids = qs.values('id')
    if request is not None:
        flag_id = request.GET.get('flag_id',None)
        if flag_id is not None:
            task_action_qs = TaskAction.objects.filter(project_id__in = project_ids,status__parent__system_code = flag_type.system_code,status_id = flag_id)
            return task_action_qs.count()
        else:
            task_action_qs = TaskAction.objects.filter(project_id__in = project_ids,status__parent__system_code = flag_type.system_code)
            total_site_flag_raised = task_action_qs.exclude(status__system_code__in = ['system_status_task_status_material_green','system_status_task_status_inspection_green']).count()
            return total_site_flag_raised
    else:
        task_action_qs = TaskAction.objects.filter(project_id__in = project_ids,status__parent__system_code = flag_type.system_code)
        total_site_flag_raised = task_action_qs.exclude(status__system_code__in = ['system_status_task_status_material_green','system_status_task_status_inspection_green']).count()
        return total_site_flag_raised

@simple_tag
def total_inspection_flag_cleared_status_count(flag_type,qs,request=None):
    project_ids = qs.values('id')
    if request is not None:
        flag_id = request.GET.get('flag_id',None)
        if flag_id is not None:
            task_action_qs = TaskAction.objects.filter(project_id__in = project_ids,status__parent__system_code = flag_type.system_code,status_id = flag_id,end_time__isnull = False)
            return task_action_qs.count()
        else:
            task_action_qs = TaskAction.objects.filter(project_id__in = project_ids,status__parent__system_code = flag_type.system_code)
            total_site_flag_cleared = task_action_qs.filter(end_time__isnull = False).exclude(status__system_code__in = ['system_status_task_status_material_green','system_status_task_status_inspection_green']).count()
            return total_site_flag_cleared
    else:
        task_action_qs = TaskAction.objects.filter(project_id__in = project_ids,status__parent__system_code = flag_type.system_code)
        total_site_flag_cleared = task_action_qs.filter(end_time__isnull = False).exclude(status__system_code__in = ['system_status_task_status_material_green','system_status_task_status_inspection_green']).count()
        return total_site_flag_cleared

@simple_tag
def total_inspection_flag_balance_status_count(flag_type,qs,request=None):
    project_ids = qs.values('id')
    if request is not None:
        flag_id = request.GET.get('flag_id',None)
        if flag_id is not None:
            task_action_qs = TaskAction.objects.filter(project_id__in = project_ids,status__parent__system_code = flag_type.system_code,status_id = flag_id,end_time__isnull = True)
            return task_action_qs.count()
        else:
            task_action_qs = TaskAction.objects.filter(project_id__in = project_ids,status__parent__system_code = flag_type.system_code)
            total_site_flag_cleared = task_action_qs.filter(end_time__isnull = True).count()
            return total_site_flag_cleared
    else:
        task_action_qs = TaskAction.objects.filter(project_id__in = project_ids,status__parent__system_code = flag_type.system_code)
        total_site_flag_cleared = task_action_qs.filter(end_time__isnull = True).count()
        return total_site_flag_cleared
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    