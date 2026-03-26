from django.db import models
from core.models import User
from django.db.models.manager import EmptyManager
from organization.models import City,Region,Type,Organization
from project.models import Project
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.db.models.manager import EmptyManager
from core.models import SystemStatus
from django.utils.dateparse import parse_duration
from decimal import Decimal


class QuillTask(MPTTModel):
    serial_number = models.CharField(max_length=100, null=True, blank=True, editable=False)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On",editable=False)
    updated_on = models.DateTimeField(auto_now=True, verbose_name="Updated On",editable=False)
    created_by = models.ForeignKey(User, null=True, blank=True,  verbose_name="Created By",  on_delete=EmptyManager,related_name="c_%(app_label)s_%(class)s_related",related_query_name="c_%(app_label)s_%(class)ss",editable=False)
    updated_by = models.ForeignKey(User, null=True, blank=True,  verbose_name="Updated By", on_delete=EmptyManager,related_name="u_%(app_label)s_%(class)s_related",related_query_name="u_%(app_label)s_%(class)ss",editable=False)
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Address", editable=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    code = models.CharField(max_length=100,unique=True)
    description = models.TextField(null=True,blank=True)

    region = models.ForeignKey(Region,null=True,blank=True, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    city = models.ForeignKey(City,null=True,blank=True, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    type = models.ForeignKey(Type,null=True,blank=True, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    organization = models.ForeignKey(Organization,null=True,blank=True, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    project = models.ForeignKey(Project,null=False,blank=False, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    status = models.ForeignKey(SystemStatus,null=True,blank=True, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")

    start_date = models.DateField(blank=True, null=True, verbose_name="SD Planned")
    end_date = models.DateField(blank=True, null=True, verbose_name="ED Planned")
    duration = models.DurationField(blank=True, null=True)

    finished_time = models.DateTimeField(blank=True, null=True,editable=False)
    finished_duration = models.DurationField(blank=True, null=True,editable=False)

    progress_planned = models.DecimalField(default=0.0,max_digits = 5,decimal_places = 2,blank=True, null=True, verbose_name="Planned Progress")
    progress_actual = models.DecimalField(default=0.0,max_digits = 5,decimal_places = 2,blank=True, null=True, verbose_name="Actual Progress")
    start_date_actual = models.DateField(blank=True, null=True)
    end_date_actual = models.DateField(blank=True, null=True)
    start_date_planned_revised = models.DateField(blank=True, null=True, verbose_name="SD Revised")
    end_date_planned_revised = models.DateField(blank=True, null=True, verbose_name="ED Revised")
    progress_planned_revised = models.DecimalField(default=0.0,max_digits = 5,decimal_places = 2,blank=True, null=True, verbose_name="Revised Progress")
    latitude = models.DecimalField(max_digits=9, decimal_places=6,null=True,blank=True,editable=False)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,null=True,blank=True,editable=False)
    precision = models.FloatField(blank=True, null=True)
    ground_monitoring = models.BooleanField(default=False)
    is_outcome = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    weight = models.FloatField(blank=True, null=True)
    effort = models.FloatField(blank=True, null=True, max_length=53, verbose_name='Effort')
    cost_planned = models.FloatField(blank=True, null=True, max_length=53, verbose_name='Planned Cost(PKR M)')
    cost = models.FloatField(blank=True, null=True, max_length=53, verbose_name='Actual Cost (PKR M)')
    from_template = models.BooleanField(default=False, blank=True, null=True)
    is_target_based = models.BooleanField(default=False)

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,on_delete=EmptyManager)
    lft = models.IntegerField(default=0, blank=True, null=True, editable=False)
    rght = models.IntegerField(default=0, blank=True, null=True, editable=False)
    tree_id = models.IntegerField(default=0, blank=True, null=True, editable=False)
    mptt_level = models.IntegerField(default=0, blank=True, null=True, editable=False)

    @property
    def show_progress_planned(self):
        from project.utils.TaskProgress import CalculateProgressMonth
        self.progress_planned = CalculateProgressMonth(self.start_date,self.end_date)
        self.save()
        return self.progress_planned

    def save(self, *args, **kwargs):

        if self.serial_number is None or len(self.serial_number) < 1:
            from project.utils.SerialNumber import getTaskSerialNumber
            self.serial_number = getTaskSerialNumber()
        
        project = self.project
        task_qs = project.project_task_related.all()
        total_tasks = task_qs.count()
        individual_task_weightage = 100/int(total_tasks)
        project_progress_list = []
        for ele in task_qs:
            if ele.progress_actual is not None:
                project_progress_list.append(int(ele.progress_actual / int(individual_task_weightage)) * 100)
        
        project_progress = Decimal(sum(project_progress_list))
        project.progress_actual = project_progress
        project.save()
        super(QuillTask, self).save(*args, **kwargs)

    class MPTTMeta:
        order_insertion_by = ['mptt_level']
        level_attr = 'mptt_level'

    class params:
        db = 'quill_bcms'
    class Meta:
        managed = False
        ordering = ['mptt_level']
        unique_together = (('code','organization',))
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        db_table = 'pro_tasks'

    def __str__(self):
        return str(self.name)
