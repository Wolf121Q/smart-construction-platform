import base64
from django import template
# from online_member_service.settings import get_avatar_base
# from membership.models import Member
# from django_middleware_global_request.middleware import get_request

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

#avatar
@simple_tag
def get_user_avatar():
    pass
    # avatar_str = ""
    # request = get_request()
    # if request.user.is_authenticated:
    #     if request.user.avatar is not None and request.user.avatar:
    #         base64_encode = base64.b64encode(request.user.avatar.read())
    #         avatar_str = "data:image/png;base64,"+base64_encode.decode('utf-8')
    #     else:
    #         avatar_str= get_avatar_base()
    # return avatar_str

@simple_tag
def get_profile_avatar():
    pass
    # avatar_str = ""
    # request = get_request()
    # if request.user.is_authenticated:
    #     if request.user.membership_profile_related is not None and request.user.membership_profile_related:
    #         if request.user.membership_profile_related.avatar is not None and request.user.membership_profile_related.avatar:
    #             base64_encode = base64.b64encode(request.user.membership_profile_related.avatar.read())
    #             avatar_str = "data:image/png;base64,"+base64_encode.decode('utf-8')
    #         else:
    #             avatar_str = get_avatar_base()
    #     else:
    #         avatar_str = get_avatar_base()
    # return avatar_str