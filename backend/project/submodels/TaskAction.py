from core.models import User
from datetime import datetime
from django.db import models
import uuid

from project.models import Project,TaskType,TaskStatus,Task

class TasktActionManager(models.Manager):
    def get_queryset(self):
        return super(TasktActionManager, self).get_queryset().filter()

class TaskAction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On",db_index=True)
    updated_on = models.DateTimeField(auto_now=True, verbose_name="Updated On")

    created_by = models.ForeignKey(User, null=True,blank=True, verbose_name="Created By", on_delete=models.CASCADE,related_name="c_%(app_label)s_%(class)s_related",related_query_name="c_%(app_label)s_%(class)ss")
    updated_by = models.ForeignKey(User, null=True,blank=True, verbose_name="Updated By", on_delete=models.CASCADE,related_name="u_%(app_label)s_%(class)s_related",related_query_name="u_%(app_label)s_%(class)ss")
    parent = models.ForeignKey('self', null=True,blank=True, verbose_name="Parent", on_delete=models.CASCADE,related_name="parent_%(app_label)s_%(class)s_related",related_query_name="parent_%(app_label)s_%(class)ss")

    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Address")
    task = models.ForeignKey(Task, null=True,blank=True, verbose_name="Task", on_delete=models.CASCADE,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")

    serial_number = models.CharField(max_length=100, null=True, blank=True, verbose_name="Serial Number",editable=False)
    project = models.ForeignKey(Project,editable=True, null=True,blank=True, verbose_name="Project", on_delete=models.CASCADE,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    type = models.ForeignKey(TaskType,editable=True, null=True,blank=True, verbose_name="Type", on_delete=models.CASCADE,related_name="type_%(app_label)s_%(class)s_related",related_query_name="type_%(app_label)s_%(class)ss")
    status = models.ForeignKey(TaskStatus,editable=True, null=True,blank=True, verbose_name="Flag", on_delete=models.CASCADE,related_name="status_%(app_label)s_%(class)s_related",related_query_name="status_%(app_label)s_%(class)ss")
    start_time = models.DateTimeField(verbose_name="Start Time",null=True,blank=True)
    end_time = models.DateTimeField(verbose_name="End Time",null=True,blank=True)
    duration = models.DurationField(verbose_name="Status Duration",null=True,blank=True)
    start_progress = models.DecimalField(default=0.0,max_digits = 5,decimal_places = 2,blank=True, null=True, verbose_name="Start Progress")
    end_progress = models.DecimalField(default=0.0,max_digits = 5,decimal_places = 2,blank=True, null=True, verbose_name="End Progress")
    progress_planned = models.DecimalField(default=0.0,max_digits = 5,decimal_places = 2,blank=True, null=True, verbose_name="Planned Progress")
    progress_actual = models.DecimalField(default=0.0,max_digits = 5,decimal_places = 2,blank=True, null=True, verbose_name="Actual Progress")
    progress_duration = models.DurationField(verbose_name="Progress Duration",null=True,blank=True)
    description = models.TextField(verbose_name="Observation",null=True,blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,null=True,blank=True,editable=False)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,null=True,blank=True,editable=False)
    precision = models.FloatField(blank=True, null=True)
    is_seen = models.BooleanField(default=False)
    seen_by = models.ForeignKey(User, null=True,blank=True, verbose_name="Seen By", on_delete=models.CASCADE,related_name="sbu_%(app_label)s_%(class)s_related",related_query_name="sbu_%(app_label)s_%(class)ss")
    seen_on = models.DateTimeField(auto_now=True, verbose_name="Seen On",null=True)
    objects = TasktActionManager()

    def save(self, *args, **kwargs):
        if self.serial_number is None:
            from project.utils.SerialNumber import getTaskActionSerialNumber
            self.serial_number = getTaskActionSerialNumber()
        # self.description = self.description.capitalize()
        super(TaskAction, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.serial_number)

    class Meta:
        verbose_name = 'Task Action'
        verbose_name_plural = 'Task Actions'
        db_table = 'pro_task_actions'
