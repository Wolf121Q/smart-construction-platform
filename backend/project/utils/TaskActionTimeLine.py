from datetime import datetime,timedelta
from django.db.models import Subquery
from project.models import TaskAction

def CalculateTaskActionTimeLineRaised(status,qs,time_line):
    days = time_line.time_line//24
    days_before_date = (datetime.now()-timedelta(days=days)).date()
    total_flags = TaskAction.objects.filter(project_id__in = Subquery(qs.values('id')),status_id=status.id,created_on__date__gte = days_before_date).count()
    if total_flags is not None and total_flags > 0:
        return total_flags
    else:
        return 0

def CalculateTaskActionTimeLineCleared(status,qs,time_line):
    days = time_line.time_line//24
    days_before_date = (datetime.now()-timedelta(days=days)).date()
    total_flags = TaskAction.objects.filter(project_id__in = Subquery(qs.values('id')),status_id=status.id,created_on__date__gte = days_before_date,end_time__isnull = False).count()
    if total_flags is not None and total_flags > 0:
        return total_flags
    else:
        return 0
    
def CalculateTaskActionTimeLineBalance(status,qs,time_line):
    balance_flags = CalculateTaskActionTimeLineRaised(status,qs,time_line) - CalculateTaskActionTimeLineCleared(status,qs,time_line)
    if balance_flags is not None and balance_flags > 0:
        return balance_flags
    else:
        return 0
    