from django.http import HttpResponse
from datetime import datetime
from project.models import TaskAction
from utils.IP import get_client_ip
from utils.pdf_utils import render_pdf_view
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from django.conf import settings
import base64
# from include.getIP import get_client_ip
# from include.CryptQRCode import CryptQR
# from application_form.models import NationalIdentityExtra,ContactDetail,Address,LegalHeir
# from housing_society.models import Type

def generate_project_report_pdf(modeladmin, request, queryset):
    ip = get_client_ip(request)
    param_request = {}
    title = ""
    heading_title = "Housing Directorate"
    param_request['organization_logo'] = ""

    # if organization is not None:
    #     title = organization.name + " " + heading_title

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
    
    logo_image_path = os.path.join(settings.BASE_DIR, 'staticfiles', 'images', 'askari_logo.png')
    # Read the image file as binary data
    with open(logo_image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    # Construct the data URI with the Base64 encoded image
    logo_image_uri = f'data:image/jpeg;base64,{encoded_image}'

        
    data = {
        'today': datetime.date,
        'param_request': param_request,
        'request': request,
        'rectified_flags' : queryset,
        'title': title,
        'heading_title': heading_title,
        'ip': ip,
        'projects' : queryset,
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
    template = get_template('pdf/rectified_flag_report.html')
    # get the context for the template
    context = data
    # render the template
    rendered_template = template.render(context)

    # create a response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="flag_report.pdf"'

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

generate_project_report_pdf.short_description = "Generate Report"