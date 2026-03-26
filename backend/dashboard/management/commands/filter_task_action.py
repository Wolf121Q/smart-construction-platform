from sys import flags
from django.core.management.base import BaseCommand
from project.models import TaskAction,TaskFile
import csv
from django.db.models import Q

class Command(BaseCommand):
    help = 'Generate a list of TaskAction instances based on specified rules'

    def handle(self, *args, **options):
        # Define the path to the output CSV file
        output_csv_file = 'defective_flag_list.csv'

        # Query to filter flags and their parent flags
        flags = TaskAction.objects.filter(
                ~Q(status__system_code__contains='green') & 
                Q(end_time__isnull=True)     
        ).exclude(status__isnull=True)

        green_flags = TaskAction.objects.filter(
            Q(status__system_code__contains='green') &       # color is Green
            Q(parent__isnull=False) &
            ~Q(parent__status__system_code__contains='green') & 
            Q(parent__end_time__isnull=False)
        )

        # Retrieve parent flags of green flags
        parent_flags = TaskAction.objects.filter(
            id__in=green_flags.values_list('parent_id', flat=True)
        )

        qs = flags | green_flags
        flags_to_keep = qs | parent_flags
        flags_to_keep = flags_to_keep.exclude(status__isnull=True)

        flags_to_keep_others = flags_to_keep.filter(~Q(status__system_code__contains='green'),parent__isnull=False,end_time__isnull=False) 
        flags_to_keep_parent_flags = TaskAction.objects.filter(
            id__in=flags_to_keep_others.values_list('parent_id', flat=True)
        )

        flags_to_keep = flags_to_keep.exclude(id__in=flags_to_keep_others)
        flags_to_keep = flags_to_keep.exclude(id__in=flags_to_keep_parent_flags)

        # Delete flags that do not meet the conditions
        TaskAction.objects.exclude(id__in=flags_to_keep).delete()

        self.stdout.write(self.style.SUCCESS('Task list generated successfully!'))
