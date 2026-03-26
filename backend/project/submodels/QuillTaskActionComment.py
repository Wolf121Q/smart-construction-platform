from core.models import User
from django.db import models
import uuid
from project.models import Project,Task, TaskAction,TaskType,TaskStatus
from django.db.models.manager import EmptyManager

class QuillTaskActionCommentManager(models.Manager):
    def get_queryset(self):
        return super(QuillTaskActionCommentManager, self).get_queryset().filter()

class QuillTaskActionComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On")
    updated_on = models.DateTimeField(auto_now=True, verbose_name="Updated On")

    created_by = models.ForeignKey(User, null=True,blank=True, verbose_name="Created By", on_delete=models.CASCADE,related_name="c_%(app_label)s_%(class)s_related",related_query_name="c_%(app_label)s_%(class)ss")
    updated_by = models.ForeignKey(User, null=True,blank=True, verbose_name="Updated By", on_delete=models.CASCADE,related_name="u_%(app_label)s_%(class)s_related",related_query_name="u_%(app_label)s_%(class)ss")
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Address")
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', db_index=True,on_delete=EmptyManager, editable=False)
    serial_number = models.CharField(max_length=100, null=True, blank=True, verbose_name="Serial Number",editable=False)
    reply = models.BooleanField(default=False,null=True,blank=True)
    project = models.ForeignKey(Project,editable=True, null=True,blank=True, verbose_name="Complaint", on_delete=models.CASCADE,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    task = models.ForeignKey(Task,editable=True, null=True,blank=True, verbose_name="Complaint Action", on_delete=models.CASCADE,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    task_action = models.ForeignKey(TaskAction,editable=True, null=True,blank=True, verbose_name="Complaint Action", on_delete=models.CASCADE,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    type = models.ForeignKey(TaskType,editable=True, null=True,blank=True, verbose_name="Type", on_delete=models.CASCADE,related_name="type_%(app_label)s_%(class)s_related",related_query_name="type_%(app_label)s_%(class)ss")
    status = models.ForeignKey(TaskStatus,editable=True, null=True,blank=True, verbose_name="status_Status", on_delete=models.CASCADE,related_name="status_%(app_label)s_%(class)s_related",related_query_name="status_%(app_label)s_%(class)ss")
    progress_planned = models.DecimalField(default=0.0,max_digits = 5,decimal_places = 2,blank=True, null=True, verbose_name="Planned Progress")
    progress_actual = models.DecimalField(default=0.0,max_digits = 5,decimal_places = 2,blank=True, null=True, verbose_name="Actual Progress")
    duration = models.DurationField(verbose_name="Progress Duration",null=True,blank=True)
    description = models.TextField(verbose_name="Action Comments",null=True,editable=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,null=True,blank=True,editable=False)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,null=True,blank=True,editable=False)
    precision = models.FloatField(default=0,blank=True, null=True)
    material_name = models.CharField(max_length=100,blank=True, null=True)
    quantity_type = models.CharField(max_length=100,blank=True, null=True)
    actual_quantity = models.DecimalField(default=0.0,max_digits = 5,decimal_places = 2,blank=True, null=True)
    damage_quantity = models.DecimalField(default=0.0,max_digits = 5,decimal_places = 2,blank=True, null=True)
    received_quantity = models.DecimalField(default=0.0,max_digits = 5,decimal_places = 2,blank=True, null=True)
    is_acknowledged = models.BooleanField(default=True,verbose_name="Critical Observation Check")
    tag_to = models.ForeignKey(User, null=True,blank=True, verbose_name="Tag To", on_delete=models.CASCADE,related_name="tag_to_%(app_label)s_%(class)s_related",related_query_name="tag_to_%(app_label)s_%(class)ss")
    tag_from = models.ForeignKey(User, null=True,blank=True, verbose_name="Tag From", on_delete=models.CASCADE,related_name="tag_from_%(app_label)s_%(class)s_related",related_query_name="tag_from_%(app_label)s_%(class)ss")
    tag_time = models.DateTimeField(verbose_name="Tag Time",null=True,blank=True)
    tag_seen = models.BooleanField(default='False',null='True',blank='True',verbose_name="Tag Seen Status")
    objects = QuillTaskActionCommentManager()

    def save(self, *args, **kwargs):
        if self.serial_number is None:
            from project.utils.SerialNumber import getTaskActionCommentSerialNumber
            self.serial_number = getTaskActionCommentSerialNumber()
        super(QuillTaskActionComment, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.serial_number)

    class params:
        db = 'quill_bcms'
    class Meta:
        managed = False
        verbose_name = 'Task Action Comment'
        verbose_name_plural = 'Task Action Comments'
        db_table = 'pro_task_action_comment'
