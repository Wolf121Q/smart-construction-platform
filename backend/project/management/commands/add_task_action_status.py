
from django.core.management.base import BaseCommand
from project.models import TaskStatus,TaskType
from core.models import User


class Command(BaseCommand):
    help = 'Creates task status'

    def handle(self, *args, **options):
        # Define data for multiple parents and their associated children
        superuser = User.objects.filter(is_superuser=True).first()
        parents_data = [
            {
                "name": "SCM",  # Replace with appropriate parent data
                "color": "#FF0000",
                "code": "system_status_task_status_scm",
                "system_code": "system_status_task_status_scm",
                "created_by": superuser,
                "status": "active",
                "type_system_code": "system_type_task_type_scm",
                "children_data": [
                    {
                        "name": "Red",
                        "color": "#FF0000",
                        "code": "system_status_task_status_scm_red",
                        "system_code": "system_status_task_status_scm_red",
                        "created_by": superuser,
                        "status": "active",
                        "type_system_code": "system_type_task_type_scm",
                    },
                    {
                        "name": "Brown",
                        "color": "#BB6000",
                        "code": "system_status_task_status_scm_brown",
                        "system_code": "system_status_task_status_scm_brown",
                        "created_by": superuser,
                        "status": "active",
                        "type_system_code": "system_type_task_type_scm",
                    },
                    {
                        "name": "Yellow",
                        "color": "#FFFD00",
                        "code": "system_status_task_status_scm_yellow",
                        "system_code": "system_status_task_status_scm_yellow",
                        "created_by": superuser,
                        "status": "active",
                        "type_system_code": "system_type_task_type_scm",

                    },
                    {
                        "name": "Green",
                        "color": "#0BFF00",
                        "code": "system_status_task_status_scm_green",
                        "system_code": "system_status_task_status_scm_green",
                        "created_by": superuser,
                        "status": "active",
                        "type_system_code": "system_type_task_type_scm",
                    },
                ]
            },
            {
                "name": "HSE",  # Replace with appropriate parent data
                "color": "#FF0000",
                "code": "system_status_task_status_hse",
                "system_code": "system_status_task_status_hse",
                "created_by": superuser,
                "status": "active",
                "type_system_code": "system_type_task_type_hse",
                "children_data": [
                    {
                        "name": "Red",
                        "color": "#FF0000",
                        "code": "system_status_task_status_hse_red",
                        "system_code": "system_status_task_status_hse_red",
                        "created_by": superuser,
                        "status": "active",
                        "type_system_code": "system_type_task_type_hse",
                    },
                    {
                        "name": "Brown",
                        "color": "#BB6000",
                        "code": "system_status_task_status_hse_brown",
                        "system_code": "system_status_task_status_hse_brown",
                        "created_by": superuser,
                        "status": "active",
                        "type_system_code": "system_type_task_type_hse",
                    },
                    {
                        "name": "Yellow",
                        "color": "#FFFD00",
                        "code": "system_status_task_status_hse_yellow",
                        "system_code": "system_status_task_status_hse_yellow",
                        "created_by": superuser,
                        "status": "active",
                        "type_system_code": "system_type_task_type_hse",

                    },
                    {
                        "name": "Green",
                        "color": "#0BFF00",
                        "code": "system_status_task_status_hse_green",
                        "system_code": "system_status_task_status_hse_green",
                        "created_by": superuser,
                        "status": "active",
                        "type_system_code": "system_type_task_type_hse",
                    }
                ]
            },
            {
                "name": "Gen Insp",  # Replace with appropriate parent data
                "color": "#FF0000",
                "code": "system_status_task_status_gen_insp",
                "system_code": "system_status_task_status_gen_insp",
                "created_by": superuser,
                "status": "active",
                "type_system_code": "system_type_task_type_gen_insp",
                "children_data": [
                    {
                        "name": "Red",
                        "color": "#FF0000",
                        "code": "system_status_task_status_gen_insp_red",
                        "system_code": "system_status_task_status_gen_insp_red",
                        "created_by": superuser,
                        "status": "active",
                        "type_system_code": "system_type_task_type_gen_insp",
                    },
                    {
                        "name": "Brown",
                        "color": "#BB6000",
                        "code": "system_status_task_status_gen_insp_brown",
                        "system_code": "system_status_task_status_gen_insp_brown",
                        "created_by": superuser,
                        "status": "active",
                        "type_system_code": "system_type_task_type_gen_insp",
                    },
                    {
                        "name": "Yellow",
                        "color": "#FFFD00",
                        "code": "system_status_task_status_gen_insp_yellow",
                        "system_code": "system_status_task_status_gen_insp_yellow",
                        "created_by": superuser,
                        "status": "active",
                        "type_system_code": "system_type_task_type_gen_insp",

                    },
                    {
                        "name": "Green",
                        "color": "#0BFF00",
                        "code": "system_status_task_status_gen_insp_green",
                        "system_code": "system_status_task_status_gen_insp_green",
                        "created_by": superuser,
                        "status": "active",
                        "type_system_code": "system_type_task_type_gen_insp",
                    }
                ]
            },
            {
                "name": "Design Insp",  # Replace with appropriate parent data
                "color": "#FF0000",
                "code": "system_status_task_status_design_insp",
                "system_code": "system_status_task_status_design_insp",
                "created_by": superuser,
                "status": "active",
                "type_system_code": "system_type_task_type_design_insp",
                "children_data": [
                    {
                        "name": "Red",
                        "color": "#FF0000",
                        "code": "system_status_task_status_design_insp_red",
                        "system_code": "system_status_task_status_design_insp_red",
                        "created_by": superuser,
                        "status": "active",
                        "type_system_code": "system_type_task_type_design_insp",
                    },
                    {
                        "name": "Brown",
                        "color": "#BB6000",
                        "code": "system_status_task_status_design_insp_brown",
                        "system_code": "system_status_task_status_design_insp_brown",
                        "created_by": superuser,
                        "status": "active",
                        "type_system_code": "system_type_task_type_design_insp",
                    },
                    {
                        "name": "Yellow",
                        "color": "#FFFD00",
                        "code": "system_status_task_status_design_insp_yellow",
                        "system_code": "system_status_task_status_design_insp_yellow",
                        "created_by": superuser,
                        "status": "active",
                        "type_system_code": "system_type_task_type_design_insp",

                    },
                    {
                        "name": "Green",
                        "color": "#0BFF00",
                        "code": "system_status_task_status_design_insp_green",
                        "system_code": "system_status_task_status_design_insp_green",
                        "created_by": superuser,
                        "status": "active",
                        "type_system_code": "system_type_task_type_design_insp",
                    }
                ]
            }
        ]

        # Create parent instances and associated child instances
        for parent_data in parents_data:
            parent_instance = TaskStatus.objects.create(
                name=parent_data['name'],
                color=parent_data['color'],
                code=parent_data['code'],
                system_code=parent_data['system_code'],
                type = TaskType.objects.filter(system_code = parent_data['type_system_code']).first(),
                created_by = parent_data['created_by'],
                status = parent_data['status'],
            )
            for child_data in parent_data['children_data']:
                TaskStatus.objects.create(
                    name=child_data['name'],
                    color=child_data['color'],
                    code=child_data['code'],
                    system_code=child_data['system_code'],
                    type=TaskType.objects.filter(system_code=child_data['type_system_code']).first(),
                    created_by=child_data['created_by'],
                    status=child_data['status'],
                    parent=parent_instance
                )

        self.stdout.write(self.style.SUCCESS('Successfully created task status instances'))

