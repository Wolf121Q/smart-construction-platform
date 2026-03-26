from django.conf import settings
from django import template
from django.http import QueryDict
from django.db.models import Exists, OuterRef
from django.utils.safestring import mark_safe
from project.models import TaskAction 

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

@register.filter()
def query_filter(value, attr):
    return value.filter(**eval(attr))

@register.filter
def flag_count(qs, flag):
    # Get a list of primary keys of TaskActions that have a related TaskFile
    filtered_qs = qs.filter(project_taskfiles__isnull=False,status=flag,end_time__isnull=True,parent__isnull=True).distinct()
    return filtered_qs.count()

@register.filter
def flag_qs(qs):
    filtered_qs = qs.filter(project_taskfiles__isnull=False,end_time__isnull=True,parent__isnull=True).distinct()
    return filtered_qs.order_by('-created_on')

@register.filter
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)

@register.filter
def divisibleby(value, arg):
    try:
        return int(value) % int(arg) == 0
    except (ValueError, ZeroDivisionError):
        return None