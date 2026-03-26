from core.models import User
from django.db import models
import uuid
from mptt.models import TreeForeignKey
from core.models import UserType
from project.models import FlagType

class TasktActionTimeLineManager(models.Manager):
    def get_queryset(self):
        return super(TasktActionTimeLineManager, self).get_queryset().filter()

class TaskActionTimeLine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On")
    updated_on = models.DateTimeField(auto_now=True, verbose_name="Updated On")
    created_by = models.ForeignKey(User, null=True,blank=True, verbose_name="Created By", on_delete=models.CASCADE,related_name="c_%(app_label)s_%(class)s_related",related_query_name="c_%(app_label)s_%(class)ss")
    updated_by = models.ForeignKey(User, null=True,blank=True, verbose_name="Updated By", on_delete=models.CASCADE,related_name="u_%(app_label)s_%(class)s_related",related_query_name="u_%(app_label)s_%(class)ss")
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Address")

    user_type = TreeForeignKey(UserType, null=True, blank=False,verbose_name="User Type", on_delete=models.CASCADE,related_name="ut_%(app_label)s_%(class)s_related",related_query_name="ut_%(app_label)s_%(class)ss")
    flag_type = models.ManyToManyField(FlagType,blank=False,related_name="ft_%(app_label)s_%(class)s_related",related_query_name="ft_%(app_label)s_%(class)ss")
    time_line = models.DurationField(null=True,blank=False,verbose_name="Time Line (Days-Hours-Minute-Seconds)")

    objects = TasktActionTimeLineManager()
    
    def __str__(self):
        return str(self.user_type.name)
  
    class Meta:
        verbose_name = 'Task Action TimeLine'
        verbose_name_plural = 'Task Action TimeLine'
        db_table = 'pro_task_action_timeline'
