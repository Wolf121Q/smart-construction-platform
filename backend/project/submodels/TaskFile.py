from django.db import models
import uuid
from core.models import User
from project.models import Project, Task,TaskType,TaskStatus,TaskAction, TaskActionComment
from organization.models import Organization
from django.core.validators import FileExtensionValidator
from utils.Upload import Upload

class TaskFileManager(models.Manager):
    def get_queryset(self):
        return super(TaskFileManager, self).get_queryset().filter()

class TaskFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On")
    updated_on = models.DateTimeField(auto_now=True, verbose_name="Updated On")
 
    created_by = models.ForeignKey(User, null=True,blank=True, verbose_name="Created By", on_delete=models.CASCADE,related_name="c_%(app_label)s_%(class)s_related",related_query_name="c_%(app_label)s_%(class)ss")
    updated_by = models.ForeignKey(User, null=True,blank=True, verbose_name="Updated By", on_delete=models.CASCADE,related_name="u_%(app_label)s_%(class)s_related",related_query_name="u_%(app_label)s_%(class)ss")
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Address")

    organization = models.ForeignKey(Organization, editable=True, null=True,blank=True, verbose_name="Organization", on_delete=models.CASCADE,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")

    project = models.ForeignKey(Project,editable=True, null=True,blank=True, verbose_name="Project", on_delete=models.CASCADE,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    task = models.ForeignKey(Task,editable=True, null=True,blank=True, verbose_name="Complaint Action", on_delete=models.CASCADE,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    task_action = models.ForeignKey(TaskAction,editable=True, null=True,blank=True, verbose_name="Complaint Action", on_delete=models.CASCADE,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    task_action_comment = models.ForeignKey(TaskActionComment,editable=True, null=True,blank=True, verbose_name="Complaint Action", on_delete=models.CASCADE,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    type = models.ForeignKey(TaskType,editable=True, null=True,blank=True, verbose_name="Type", on_delete=models.CASCADE,related_name="type_%(app_label)s_%(class)s_related",related_query_name="type_%(app_label)s_%(class)ss")
    status = models.ForeignKey(TaskStatus,editable=True, null=True,blank=True, verbose_name="status_Status", on_delete=models.CASCADE,related_name="status_%(app_label)s_%(class)s_related",related_query_name="status_%(app_label)s_%(class)ss")
    progress_planned = models.DecimalField(default=0.0,max_digits = 5,decimal_places = 2,blank=True, null=True, verbose_name="Planned Progress")
    progress_actual = models.DecimalField(default=0.0,max_digits = 5,decimal_places = 2,blank=True, null=True, verbose_name="Actual Progress")
    duration = models.DurationField(verbose_name="Progress Duration",null=True,blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,null=True,blank=True,editable=False)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,null=True,blank=True,editable=False)
    precision = models.FloatField(blank=True, null=True)
    filename = models.CharField(max_length=100,null=True, blank=True)
    attachment = models.FileField(max_length=250,verbose_name="Attachment",null=True, blank=True, upload_to=Upload,validators=[FileExtensionValidator(['png','jpeg','jpg'])])
    objects = TaskFileManager()

    class Meta:
        verbose_name = 'Task File'
        verbose_name_plural = 'Task Files'
        db_table = 'pro_task_files'
