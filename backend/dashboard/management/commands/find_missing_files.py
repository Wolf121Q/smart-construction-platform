import os
from django.core.management.base import BaseCommand
from project.models import TaskFile  # Replace 'your_app' and 'TaskFile' with your actual app and model names
import csv

class Command(BaseCommand):
    help = 'Find instances with missing files'

    def handle(self, *args, **options):
        # Query all instances of your model
        instances = TaskFile.objects.all()  # Replace 'TaskFile' with your actual model name

        # Define the path to the output CSV file
        output_csv_file = 'output.csv'

        # Open the CSV file for writing
        with open(output_csv_file, mode='w', newline='') as csv_file:
            # Create a CSV writer
            csv_writer = csv.writer(csv_file)
            # Write the header row with column names
            csv_writer.writerow(['Serial Number', 'Region', 'City','Creation Time','File Path'])  # Replace with your column names

            for instance in instances:
                file_path = instance.attachment.path  # Replace 'file_field' with the name of your FileField
                # Check if the file exists
                if not os.path.exists(file_path):
                    csv_writer.writerow([instance.task_action.serial_number, instance.project.region.name, instance.project.city.name,instance.created_on,file_path])  # Replace with your field names
        
        self.stdout.write(self.style.SUCCESS(f'Successfully exported instances to {output_csv_file}'))

     