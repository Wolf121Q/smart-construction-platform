from django.db.models import Q
import os
from datetime import datetime
from core.models import SystemStatus
from project.models import TaskAction,TaskActionTimeLine,Project,TaskFile
from dashboard.utils.filterUserBasedQs import weekly_obsns_datefilter,filtered_qs_rolebased,filtered_region_rolebased,filtered_city_rolebased
from django.db.models import Exists, OuterRef

class TaskActionManager:
    def __init__(self, model, request,year=None):
        self.model = model
        self.request = request
        self.year = year

        # Filter the queryset based on the provided year
        if self.year:
            self.qs = model._default_manager.get_queryset().filter(
                project_id__in=filtered_qs_rolebased(request),
                status__isnull=False,
                created_on__year=self.year
            )
        else:
            self.qs = model._default_manager.get_queryset().filter(
                project_id__in=filtered_qs_rolebased(request),
                status__isnull=False
            )
        self.time_line_obj = TaskActionTimeLine.objects.filter(user_type=self.request.user.type).first()

    def get_filtered_task_files(self):
        filtered_task_files = [
            task_file for task_file in TaskFile.objects.all()
            if self.file_exists(task_file.attachment.path)  # Adjust the attribute name accordingly
        ]

        return filtered_task_files

    def file_exists(self, file_path):
        # Check if the file exists in the media folder
        return os.path.exists(file_path)


    def get_qs(self):
        # Remove Flags without attachments
         # Exclude TaskAction instances with related TaskActionAttachments without a file
        # print(self.get_filtered_task_files())


        # task_file_qs = TaskFile.objects.filter(attachment__isnull=False)
        # for instance in task_file_qs:
        #     file_path = instance.attachment.path
        #     if not os.path.exists(file_path):
        #         task_file_qs = task_file_qs.exclude(pk=instance.pk)

        # self.qs = self.qs.filter(id__in = task_file_qs.values('task_action_id').distinct())

        # Assuming this is part of a method in your class
        combined_queryset = self.model.objects.none()

        if self.time_line_obj:
            time_line = datetime.now() - self.time_line_obj.time_line

            if self.time_line_obj.flag_type.all().count() > 0:
                # Create a list to hold individual querysets for each flag type
                querysets = []

                for type in self.time_line_obj.flag_type.all():
                    qs = self.qs.exclude(status__type__system_code=type.system_code).filter(
                        status__type__system_code=type.system_code,
                        created_on__date__lt=time_line.date()
                    )
                    querysets.append(qs)

                # Combine all querysets without duplicates
                if querysets:
                    combined_queryset = querysets[0]
                    for qs in querysets[1:]:
                        combined_queryset = combined_queryset | qs

            # Use distinct to avoid duplicates and order the result
            return combined_queryset.order_by("-created_on")

        else:
            return self.qs.order_by("-created_on")



        # combined_queryset = self.model.objects.none()
        # if self.time_line_obj:
        #     time_line = datetime.now() - self.time_line_obj.time_line
        #     if self.time_line_obj.flag_type.all().count() > 0:
        #         for type in self.time_line_obj.flag_type.all():
        #             qs = self.qs.exclude(status__type__system_code=type.system_code)
        #             combined_queryset = combined_queryset | qs.filter(
        #                 status__type__system_code=type.system_code,
        #                 created_on__date__lt=time_line.date()
        #             )
        #     return combined_queryset.distinct().order_by("-created_on")
        # else:
        #     return self.qs

        # combined_queryset = self.model.objects.none()
        # if self.time_line_obj:
        #     time_line = datetime.now() - self.time_line_obj.time_line
        #     if self.time_line_obj.flag_type.all().count() > 0:
        #         for type in self.time_line_obj.flag_type.all():
        #             qs = self.qs.exclude(status__type__system_code = type.system_code)
        #             combined_queryset = combined_queryset | qs.filter(status__type__system_code = type.system_code,created_on__date__lt = time_line.date())
        #     return combined_queryset.order_by("-created_on")
        # else:
        #     return self.qs

    def get_rectified_flags(self):
        # Filter for rectified flags
        #rectified_qs = TaskAction.objects.filter(parent_id__in = self.get_qs().filter(end_time__isnull=False,parent__isnull=True,project__region__status='active',project__city__status='active'))
        rectified_qs = self.get_qs().filter(end_time__isnull=False,parent__isnull=True,project__region__status='active',project__city__status='active',status__parent__system_code__in = ['system_status_task_status_inspection','system_status_task_status_material'])
        return rectified_qs.order_by('-created_on')

    def get_pending_flags(self):
        qs = self.get_qs().filter(end_time__isnull=True,parent__isnull=True)
        return qs.order_by('-created_on')
    
    def get_inspection_flags_stats(self):
        # Inspection Flag Card Filter
        inspection_flags_counts = []
        inspection_flags_counts_raised = 0
        inspection_flags_counts_cleared = 0
        inspection_flags_counts_balance = 0
        for ins_flag in SystemStatus.objects.filter(system_code = "system_status_task_status_inspection").first().get_descendants(include_self = False).exclude(system_code="system_status_task_status_inspection_green"):
            inspection_qs = self.get_qs().filter(status=ins_flag)
            inspection_pending_qs = inspection_qs
            inspection_cleared_qs = self.get_rectified_flags().filter(status=ins_flag)
            if inspection_pending_qs.exists() and inspection_cleared_qs.exists():
                inspection_raised_qs = inspection_pending_qs.union(inspection_cleared_qs)
            else:
                inspection_raised_qs = inspection_pending_qs or inspection_cleared_qs
            inspection_flags_counts_raised =    inspection_flags_counts_raised + inspection_raised_qs.count()
            inspection_flags_counts_cleared =   inspection_flags_counts_cleared + inspection_cleared_qs.count()
            inspection_flags_counts_balance =   inspection_flags_counts_balance + inspection_pending_qs.count()
            data_dict = {
                "id":str(ins_flag.id),
                "flag_color":ins_flag.color,
                "raised_count":inspection_raised_qs.count(),
                "cleared_count":inspection_cleared_qs.count(),
                "pending_count":inspection_pending_qs.count()
            }
            inspection_flags_counts.append(data_dict)
        return inspection_flags_counts
    
    def get_material_flags_stats(self):
        material_flags_counts = []
        material_flags_counts_raised = 0
        material_flags_counts_cleared = 0
        material_flags_counts_balance = 0
        for mat_flag in SystemStatus.objects.filter(system_code = "system_status_task_status_material").first().get_descendants(include_self = False).exclude(system_code="system_status_task_status_material_green"):
            material_qs = self.get_qs().filter(status=mat_flag)
            # Start with a base queryset
            material_pending_qs = material_qs
            # Calculate cleared material by excluding pending material
            material_cleared_qs = self.get_rectified_flags().filter(status=mat_flag)
            if material_pending_qs.exists() and material_cleared_qs.exists():
                material_raised_qs = material_pending_qs.union(material_cleared_qs)
            else:
                material_raised_qs = material_pending_qs or material_cleared_qs
            material_flags_counts_raised = material_flags_counts_raised + material_raised_qs.count()
            material_flags_counts_cleared = material_flags_counts_cleared + material_cleared_qs.count()
            material_flags_counts_balance = material_flags_counts_balance + material_pending_qs.count()
            data_dict = {
                "id":str(mat_flag.id),
                "flag_color":mat_flag.color,
                "raised_count":material_raised_qs.count(),
                "cleared_count":material_cleared_qs.count(),
                "pending_count":material_pending_qs.count(),
            }
            material_flags_counts.append(data_dict)
        return material_flags_counts
