from django.http import HttpResponse
from datetime import datetime
from project.models import TaskAction
from utils.IP import get_client_ip
from django.db.models import Subquery,Count,Q
from core.models import SystemStatus
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import OuterRef, Subquery, Exists
import os
from django.conf import settings
import base64
# from include.getIP import get_client_ip
# from include.CryptQRCode import CryptQR
# from application_form.models import NationalIdentityExtra,ContactDetail,Address,LegalHeir
# from housing_society.models import Type

def generate_project_report_pdf(modeladmin, request, queryset):
    ip = get_client_ip(request)
    organization = queryset[0].organization
    param_request = {}
    title = ""
    heading_title = "Housing Directorate"
    param_request['organization_logo'] = ""
    task_actions = TaskAction.objects.filter(project_id__in = Subquery(queryset.values("id")))

    # Construct the full URL to the askari logo image

    logo_image_path = os.path.join(settings.BASE_DIR, 'staticfiles', 'images', 'askari_logo.png')
    # Read the image file as binary data
    with open(logo_image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    # Construct the data URI with the Base64 encoded image
    logo_image_uri = f'data:image/jpeg;base64,{encoded_image}'
    
    # Get all projects that have at least one reference in the TaskAction model
    queryset = queryset.annotate(
        has_task_actions=Exists(TaskAction.objects.filter(project=OuterRef('pk')).exclude(status__system_code__in = ['system_status_task_status_material_green','system_status_task_status_inspection_green']))
    ).filter(has_task_actions=True)


    if organization is not None:
        title = organization.name + " " + heading_title

            # param_request['avatar'] = ""
            # if application_form is not None:
            #     if len(str(application_form.avatar_thumbnail)) > 0:
            #         param_request['avatar'] = getImagePathBase64(application_form.avatar.path)


            # if bool(request.GET.get('created_by', False)) == True:
            #     param_request['created_by'] = request.GET['author']
            # else:
            #     param_request['created_by'] = ""

            # qr_code_str = str(application_form.serial_number)
            # qrcode_path = CryptQR(application_form.society, qr_code_str, 2)

        #     national_identity = NationalIdentityExtra.objects.filter(application_form_id=application_form.id).first()
        #     national_identities = NationalIdentityExtra.objects.filter(application_form_id=application_form.id)
        #     contact_details = ContactDetail.objects.filter(application_form_id=application_form.id)
        #     addresses = Address.objects.filter(application_form_id=application_form.id)
        #     next_of_kin = LegalHeir.objects.filter(type='next_of_kin',application_form_id=application_form.id)
        #     legal_heirs = LegalHeir.objects.filter(type='legal_heirs',application_form_id=application_form.id)
        #     terms_and_conditions = Type.objects.filter(system_code = 'app_form_pdf',status='active').first()
        
        total_inspection_flags = TaskAction.objects.filter(project_id__in = Subquery(queryset.values("id"))).aggregate(
            
            red = Count(
                'pk', filter=Q(status__system_code__in = ['system_status_task_status_inspection_red'],end_time__isnull=True)
            ),
          
            brown=Count(
                'pk', filter=Q(status__system_code__in = ['system_status_task_status_inspection_yellow'],end_time__isnull=True)
            ),
          
            yellow=Count(
                'pk', filter=Q(status__system_code__in = ['system_status_task_status_inspection_orange'],end_time__isnull=True)
            ),
           
            green=Count(
                'pk', filter=Q(status__system_code__in = ['system_status_task_status_material_green'],end_time__isnull=True)
            )
        )


        total_material_flags = TaskAction.objects.filter(project_id__in = Subquery(queryset.values("id"))).aggregate(
            red = Count(
                'pk', filter=Q(status__system_code__in = ['system_status_task_status_material_red'],end_time__isnull=True)
            ),
            yellow=Count(
                'pk', filter=Q(status__system_code__in = ['system_status_task_status_material_yellow'],end_time__isnull=True)
            ),
            orange=Count(
                'pk', filter=Q(status__system_code__in = ['system_status_task_status_material_orange'],end_time__isnull=True)
            ),
            green=Count(
                'pk', filter=Q(status__system_code__in = ['system_status_task_status_material_green'],end_time__isnull=True)
            ),
        )

        parent_flags = SystemStatus.objects.filter(system_code__in = ["system_status_task_status_material","system_status_task_status_inspection"])
      
        data = {
            'today': datetime.date,
            'param_request': param_request,
            'request': request,
            'organization': organization,
            'projects' : queryset,
            'title': title,
            'heading_title': heading_title,
            'ip': ip,
            'total_inspection_flags':total_inspection_flags,
            'total_material_flags':total_material_flags,
            'parent_flags':parent_flags,
            'logo_url':logo_image_uri,
            # 'qrcode_path': qrcode_path,
            # 'application_form': application_form,
            # 'national_identity': national_identity,
            # 'contact_details': contact_details,
            # 'national_identities': national_identities,
            # 'addresses': addresses,
            # 'next_of_kin': next_of_kin,
            # 'legal_heirs': legal_heirs,
            # 'terms_and_conditions': terms_and_conditions
        }

        # get the template to render
        template = get_template('pdf/ca_obsns_report.html')
        # get the context for the template
        context = data
        # render the template
        rendered_template = template.render(context)

        # create a response object
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'

        # create a PDF object
        pdf = pisa.CreatePDF(
            rendered_template,
            dest=response,
            encoding='utf-8',
            link_callback=request.build_absolute_uri,
        )
        # check if PDF creation was successful
        if not pdf.err:
            return response
        return HttpResponse('Error creating PDF: %s' % pdf.err, status=500)

generate_project_report_pdf.short_description = "Generate CA Obsn Report"