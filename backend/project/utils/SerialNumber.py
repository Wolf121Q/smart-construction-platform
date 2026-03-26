from project.models import Project,Task,TaskAction,TaskActionComment
import datetime,time,math, random

def Serial_increment(sn_number):
    if Project.objects.filter(serial_number__icontains=sn_number).count() > 0:
        sn_number = int(sn_number)
        sn_number = sn_number + 1
        sn_number = str(sn_number)
        sn_number = Serial_increment(sn_number)
    return sn_number

def getSerialNumber():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    member_count = Project.objects.filter(created_on__year=year, created_on__month=month, created_on__day=day).count()
    if member_count == 0:
        member_count = 1
    member_count = str(member_count)
    s_number = member_count.rjust(3, '0')

    s_number = str(year)+str(month).rjust(2, '0')+str(day).rjust(2, '0')+str(s_number)
    s_number = Serial_increment(s_number)
    type = "TC"
    return str(type)+str(s_number)

def Serial_task_increment(sn_number):
    if Task.objects.filter(serial_number__icontains=sn_number).count() > 0:
        sn_number = int(sn_number)
        sn_number = sn_number + 1
        sn_number = str(sn_number)
        sn_number = Serial_task_increment(sn_number)
    return sn_number

def getTaskSerialNumber():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    member_count = Task.objects.filter(created_on__year=year, created_on__month=month, created_on__day=day).count()
    if member_count == 0:
        member_count = 1
    member_count = str(member_count+1)
    s_number = member_count.rjust(3, '0')

    s_number = str(year)+str(month).rjust(2, '0')+str(day).rjust(2, '0')+str(s_number)
    s_number = Serial_task_increment(s_number)
    type = "TS"
    return str(type)+str(s_number)

def Serial_task_action_increment(sn_number):
    if TaskAction.objects.filter(serial_number__icontains=sn_number).count() > 0:
        sn_number = int(sn_number)
        sn_number = sn_number + 1
        sn_number = str(sn_number)
        sn_number = Serial_task_action_increment(sn_number)
    return sn_number

def getTaskActionSerialNumber():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    member_count = TaskAction.objects.filter(created_on__year=year, created_on__month=month, created_on__day=day).count()
    if member_count == 0:
        member_count = 1
    member_count = str(member_count+1)
    s_number = member_count.rjust(3, '0')

    s_number = str(year)+str(month).rjust(2, '0')+str(day).rjust(2, '0')+str(s_number)
    s_number = Serial_task_action_increment(s_number)
    type = "TAS"
    return str(type)+str(s_number)


def Serial_task_action_comment_increment(sn_number):
    if TaskActionComment.objects.filter(serial_number__icontains=sn_number).count() > 0:
        sn_number = int(sn_number)
        sn_number = sn_number + 1
        sn_number = str(sn_number)
        sn_number = Serial_task_action_comment_increment(sn_number)
    return sn_number

def getTaskActionCommentSerialNumber():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    member_count = TaskActionComment.objects.filter(created_on__year=year, created_on__month=month, created_on__day=day).count()
    if member_count == 0:
        member_count = 1
    member_count = str(member_count+1)
    s_number = member_count.rjust(3, '0')

    s_number = str(year)+str(month).rjust(2, '0')+str(day).rjust(2, '0')+str(s_number)
    s_number = Serial_task_action_comment_increment(s_number)
    type = "TACS"
    return str(type)+str(s_number)

def getProjectRefencenNumber(project):
    region_code =  project.region.code
    city_code = project.city.code
    organization_code = project.organization.code
    project_code = project.code
    return str(region_code).title()+"/"+str(city_code).title()+"/"+str(organization_code).title()+"-"+str(project_code)
