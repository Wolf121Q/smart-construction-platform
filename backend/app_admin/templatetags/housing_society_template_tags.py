import base64
from django import template
# from housing_society.models import Society,Type
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe
from django.conf import settings
from os import path
# from membership.models import PaymentChallan,PaymentChallanDetail,PaymentSchedule,PaymentScheduleDetail

# Depending on your django version, `reverse` and `NoReverseMatch` has been moved.
# From django 2.0 they've been moved to `django.urls`
try:
    from django.urls import reverse, NoReverseMatch
except ImportError:
    from django.core.urlresolvers import reverse, NoReverseMatch

register = template.Library()

# From django 1.9 `assignment_tag` is deprecated in favour of `simple_tag`
try:
    simple_tag = register.simple_tag
except AttributeError:
    simple_tag = register.assignment_tag

@simple_tag
def show_client_ip(request):
    from utils.IP import get_client_ip
    return get_client_ip(request)


@simple_tag
def display_logo():
    img_url = str(settings.BASE_DIR) + '/app_admin/static/assets/image/askari_logo.png'
    with open(img_url, "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
        src = "data:image/png;base64,"+my_string.decode('utf-8')
        return src

    # with open(img_url, "rb") as img_file:
    #     my_string = base64.b64encode(img_file.read())
    #     src = "data:image/png;base64,"+my_string.decode('utf-8')
    #     return src

#     logo_str = ""
#     society = Society.objects.filter(status='active').first()
#     if society is not None:
#         if society.logo is not None and society.logo:
#             base64_encode = base64.b64encode(society.logo.read())
#             logo_str = "data:image/png;base64,"+base64_encode.decode('utf-8')
#     return logo_str

@simple_tag
def display_favicon():
    img_url = str(settings.BASE_DIR) + '/app_admin/static/assets/image/askari_favicon.png'
    with open(img_url, "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
        src = "data:image/png;base64,"+my_string.decode('utf-8')
        return src

@simple_tag
def display_obsns_modal_logo():
    img_url = str(settings.BASE_DIR) + '/app_admin/static/assets/image/askari_favicon_png.png'
    with open(img_url, "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
        src = "data:image/png;base64,"+my_string.decode('utf-8')
        return src

@simple_tag
def get_attachment_base64(img_url):
    if path.exists(str(img_url)):
        with open(img_url, "rb") as img_file:
            my_string = base64.b64encode(img_file.read())
            src = "data:image/png;base64,"+my_string.decode('utf-8')
            return src
    else:
        return None



#     society = Society.objects.filter(status='active').first()
#     if society is not None:
#         if society.favicon is not None and society.favicon:
#             base64_encode = base64.b64encode(society.favicon.read())
#             logo_str = "data:image/png;base64,"+base64_encode.decode('utf-8')
#     return logo_str

# @simple_tag
# def registration_terms_condition():
#     reg_terms = Type.objects.filter(system_code='sign up',status='active').first()
#     if reg_terms:
#         return reg_terms.description
#     else:
#         return "Sorry Terms & Condition not Defined"

# # Tag for remarks popup
# @register.filter()
# def psd_remarks_popover(value, *args):
#     psd_ct = ContentType.objects.get_for_model(PaymentScheduleDetail)
#     payment_challan_detail = PaymentChallanDetail.objects.filter(content_detail_type=psd_ct,object_detail_id = value).first()
#     if payment_challan_detail is not None:
#         payment_challan         = payment_challan_detail.payment_challan
#         if payment_challan is not None:
#             if payment_challan.remarks:
#                 return mark_safe(
#                     '<button id="popover-2" class="btn px-4 btn-primary my-1" data-placement="bottom" title="" data-content={remarks} data-original-title="Finance Remarks">Finance Remarks</button>"'.format(
#                         remarks=payment_challan.remarks))
#             else:
#                 return ""
#         else:
#             return ""
#     else:
#         return ""






