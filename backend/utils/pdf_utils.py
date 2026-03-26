import os
from django.conf import settings
from django.contrib.staticfiles import finders
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import base64,os
from ConstructionManagementSystem.settings import MEDIA_ROOT

def getImagePathBase64(str_path):
    encoded_string = ""
    str_path = os.path.join(str(MEDIA_ROOT), str(str_path))
    with open(str_path, "rb") as image_file:
        #encoded_string = base64.b64encode(image_file.read())

        encoded_string = ("data:image/png;" +
                "base64," + base64.b64encode(image_file.read()).decode("utf-8"))
        return encoded_string
    return ""
def link_callback(uri, rel):
    #return os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # result = finders.find(uri)
    # if result:
    #     if not isinstance(result, (list, tuple)):
    #         result = [result]
    #     result = list(os.path.realpath(path) for path in result)
    #     path = result[0]
    # else:
    sUrl = "public/"+settings.STATIC_URL  # Typically /static/
    sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL  # Typically /media/
    mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s path: %s' % (sUrl, mUrl,path)
        )
    return path


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def render_pdf_view(template_path, context={}):
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def render_pdf_save(template_path, context={}, output_filename="Letter.pdf"):

    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=result_file, link_callback=link_callback)

    # close output file
    result_file.close()                 # close output file
    # return False on success and True on errors
    return pisa_status.err
