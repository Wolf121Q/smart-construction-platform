from django.conf import settings
from django import template
from django.http import QueryDict
from django.db.models import Exists, OuterRef
from django.utils.safestring import mark_safe

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


MAX_LENGTH_BOOTSTRAP_COLUMN = 12


def css_classes_for_field(field, custom_classes):
    orig_class = field.field.widget.attrs.get('class', '')
    required = 'required' if field.field.required else ''
    classes = field.css_classes(' '.join([orig_class, custom_classes, required]))
    return classes


@register.filter()
def get_label(field, custom_classes=''):
    #classes = css_classes_for_field(field, custom_classes)
    return field.label_tag(attrs={'class': custom_classes}, label_suffix='')


@register.filter()
def add_class(field, custom_classes=''):
    classes = css_classes_for_field(field, custom_classes)
    try:
        # For widgets like SelectMultiple, checkboxselectmultiple
        field.field.widget.widget.attrs.update({'class': classes})
    except:
        field.field.widget.attrs.update({'class': classes})
    return field


@register.filter()
def widget_type(field):
    if isinstance(field, dict):
        return 'adminreadonlyfield'
    try:
        # For widgets like SelectMultiple, checkboxselectmultiple
        widget_type = field.field.widget.widget.__class__.__name__.lower()
    except:
        widget_type = field.field.widget.__class__.__name__.lower()
    return widget_type


@register.filter()
def placeholder(field, placeholder=''):
    field.field.widget.attrs.update({'placeholder': placeholder})
    return field


def sidebar_menu_setting():
    return getattr(settings, 'BOOTSTRAP_ADMIN_SIDEBAR_MENU', True)


@simple_tag
def display_sidebar_menu(has_filters=True):
    if has_filters:
        # Always display the menu in change_list.html
        return True
    return sidebar_menu_setting()


@register.filter()
def class_for_field_boxes(line):
    size_column = MAX_LENGTH_BOOTSTRAP_COLUMN // len(line.fields)
    return 'col-sm-{0}'.format(size_column or 1)  # if '0' replace with 1



@register.filter()
def TagtoUrl(html_tage):
    url_value = ''
    start = ''
    end = ''
    if 'href=' in html_tage:
        start = '<a href="'
        end = '">'
        url_value = html_tage[html_tage.find(start) + len(start):html_tage.rfind(end)]
    elif 'src=' in html_tage:
        start = '<img src="'
        end = '">'

        url_value = html_tage[html_tage.find(start) + len(start):html_tage.rfind(end)]
    return url_value

@register.filter()
def endswithImage(value):

    if value.endswith(('.apng', '.avif', '.gif', '.jpg', '.jpeg', '.jfif', '.pjpeg', '.pjp', '.png', '.svg', '.webp')):
        return True
    else:
        return False


@register.filter()
def to_str(value):
    return str(value)

@register.filter()
def getNameAvatar(user):
    first = str(user.first_name[0]).upper()
    last = str(user.last_name[0]).upper()
    return first+last

@register.filter()
def task_action_filter_label(label):
    label_list = label.split()
    if len(label_list) > 1:
        name = " "
        for entry in label_list[:-1]:
            name += ' '+ entry
        return mark_safe(
                        '<span style="float:left">{name}</span><span class="badge badge-primary text-white text-end" style="float:right;background-color:#927ee7 !important;">{count}</span>'.format(
                            name=name,count=label_list[-1]
                        )
        
        )
    else:
        return mark_safe(
                        '<span style="float:left">{name}<span>&nbsp;&nbsp;&nbsp;<span>'.format(
                            name=label_list[-1])
        )

@register.filter()
def task_action_flag_filter_label(label):
    label_list = label.split()
    if len(label_list) > 1:
        color = " "
        for entry in label_list[:-1]:
           color += ' '+ entry
        return mark_safe(
                        '<span style="float:left"><i class="fa fa-flag" aria-hidden="true" style="color:{color};font-size:25px"></i></span><span class="badge badge-primary text-white text-end" style="float:right;background-color:#927ee7 !important;">{count}</span>'.format(
                            color=color,count=label_list[-1]
                        )
       
        )
    else:
        return mark_safe(
                        '<span style="float:left">{color}<span>&nbsp;&nbsp;&nbsp;<span>'.format(
                            color=label_list[-1])
        )


# #https://newbedev.com/how-do-i-add-multiple-arguments-to-my-custom-template-filter-in-a-django-template
# @register.filter(name='tostring')
# def template_queryset_count(things, args):
#     if args is None:
#         return False
#     qs = QueryDict(args)
#     if qs.has_key('key_name') and qs.has_key('key_value'):
#         key_name = qs['key_name']
#         key_value = qs['key_value']
#
#         filter_dict = {key_name : key_value}
#         return things.objects.filter(**filter_dict).count()
#     return 0
# register.filter(template_queryset_count)


# def query(qs, **kwargs):
#     """ template tag which allows queryset filtering. Usage:
#           {% query books author=author as mybooks %}
#           {% for book in mybooks %}
#             ...
#           {% endfor %}
#     """
#     return qs.filter(**kwargs)
#
# @simple_tag('template_query',query)

