from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from dashboard.models import TaskActionList
from core.models import SystemStatus
from django.utils.safestring import mark_safe
from django.db.models import Q
from daterange_filter.filter import DateRangeFilter
from project.models import TaskStatus, Region, City, TaskAction, TaskActionTimeLine, TaskActionComment, TaskFile, \
    Organization
from django.shortcuts import redirect
from django.urls import re_path, reverse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.utils.html import format_html
from dashboard.utils.filterUserBasedQs import filtered_project_qs_rolebased_android
from utils.IP import get_client_ip
from dashboard.utils.generateRectifiedReport import generate_project_report_pdf
from django.db.models import Count
from dashboard.utils.flag_management import TaskActionManager
from django.db.models.functions import ExtractMonth
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta
from django.utils.timezone import now
from django import forms


class TimeSinceFilterForm(forms.Form):
    CHOICES = [
        ('', 'All flags'),
        ('1_week', _('1 week ago')),
        ('1_month', _('1 month ago')),
        ('3_months', _('3 months ago')),
        ('6_months', _('6 months ago')),
    ]
    
    time_since = forms.ChoiceField(choices=CHOICES, required=False)

class FlagFilterForm(forms.Form):
    flag_form_filter_field = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        # Extract the request or any other required data
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        # Get choices from a method
        self.fields['flag_form_filter_field'].choices = self.get_task_action_choices(request)

    def get_task_action_choices(self, request):
        task_action_manager = TaskActionManager(TaskAction, request)
        qs = task_action_manager.get_pending_flags()

        statuses = set([c.status for c in qs.order_by('status__code').distinct('status__code')])
        # Lists to hold the sorted statuses
        red_statuses = []
        brown_statuses = []
        yellow_statuses = []

        # Iterate through the statuses and categorize them
        for status in statuses:
            if 'red' in status.system_code:
                red_statuses.append(status)
            elif 'orange' in status.system_code:
                brown_statuses.append(status)
            elif 'yellow' in status.system_code:
                yellow_statuses.append(status)
        # Combine the lists in the desired order
        sorted_statuses = red_statuses + brown_statuses + yellow_statuses


        if sorted_statuses is not None:
            choices = [('', 'All Flags')]  # The empty string is used for the default option
            choices.extend([(c.id, f"{c.name} ({c.parent.name})") for c in sorted_statuses])
            return choices
        return [('', 'All Flags')] 


class TimeAgoFilter(admin.SimpleListFilter):
    title = _('Pending Since')
    parameter_name = 'time_ago'

    def lookups(self, request, model_admin):
        return (
            ('1_week', _('1 week ago')),
            ('1_month', _('1 month ago')),
            ('3_months', _('3 months ago')),
            ('6_months', _('6 months ago')),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            now_time = now()
            if value == '1_week':
                start_date = now_time - timedelta(weeks=1)
            elif value == '1_month':
                start_date = now_time - timedelta(days=30)
            elif value == '3_months':
                start_date = now_time - timedelta(days=90)
            elif value == '6_months':
                start_date = now_time - timedelta(days=180)
            else:
                return queryset

            return queryset.filter(created_on__gte=start_date)
        return queryset


class PendingStatusFilter(admin.SimpleListFilter):
    title = 'Pending Flag'
    parameter_name = 'pending_flag_status'

    def lookups(self, request, model_admin):
        task_action_manager = TaskActionManager(TaskAction, request)
        qs = task_action_manager.get_pending_flags()
        statuses = set([c.status for c in qs.order_by('status__code').distinct('status__code')])
        if statuses is not None:
            return [(c.id,f"{c.name} ({c.parent.name})") for c in statuses]
        return None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset


# CUSTOM MPTT FILTER
class MaterialFlagsFilter(SimpleListFilter):
    title = 'Material Flags'
    parameter_name = 'status_id'

    def lookups(self, request, model_admin):
        children = SystemStatus.objects.filter(system_code='system_status_task_status_material').first().get_children()
        # Return a list of tuples (value, display) for the filter options
        return [(str(child.id), child.name) for child in children]

    def queryset(self, request, queryset):
        value = self.value()
        if value is not None:
            # Filter the queryset based on the selected child node
            return queryset.filter(status_id=value)

    def choices(self, changelist):
        # Override choices to display the count for each child node
        for lookup, title in self.lookup_choices:
            count = TaskActionList.objects.filter(status_id=lookup).count()
            url = reverse('admin:dashboard_taskactionlist_changelist') + f'?status_id={lookup}'
            yield {
                'selected': self.value() == lookup,
                'query_string': changelist.get_query_string({self.parameter_name: lookup}),
                'display': format_html(f'{title}({count})')
            }


class InspectionFlagsFilter(SimpleListFilter):
    title = 'Inspection Flags'
    parameter_name = 'status_id'

    def lookups(self, request, model_admin):
        children = SystemStatus.objects.filter(
            system_code='system_status_task_status_inspection').first().get_children()
        # Return a list of tuples (value, display) for the filter options
        return [(str(child.id), child.name) for child in children]

    def queryset(self, request, queryset):
        value = self.value()
        if value is not None:
            # Filter the queryset based on the selected child node
            return queryset.filter(status_id=value)

    def choices(self, changelist):
        # Override choices to display the count for each child node
        for lookup, title in self.lookup_choices:
            count = TaskActionList.objects.filter(status_id=lookup).count()
            url = reverse('admin:dashboard_taskactionlist_changelist') + f'?status_id={lookup}'
            yield {
                'selected': self.value() == lookup,
                'query_string': changelist.get_query_string({self.parameter_name: lookup}),
                'display': format_html(f'{title}({count})')
            }


class HseFlagsFilter(SimpleListFilter):
    title = 'HSE Flags'
    parameter_name = 'status_id'

    def lookups(self, request, model_admin):
        children = SystemStatus.objects.filter(
            system_code='system_status_task_status_hse').first().get_children()
        # Return a list of tuples (value, display) for the filter options
        return [(str(child.id), child.name) for child in children]

    def queryset(self, request, queryset):
        value = self.value()
        if value is not None:
            # Filter the queryset based on the selected child node
            return queryset.filter(status_id=value)

    def choices(self, changelist):
        # Override choices to display the count for each child node
        for lookup, title in self.lookup_choices:
            count = TaskActionList.objects.filter(status_id=lookup).count()
            url = reverse('admin:dashboard_taskactionlist_changelist') + f'?status_id={lookup}'
            yield {
                'selected': self.value() == lookup,
                'query_string': changelist.get_query_string({self.parameter_name: lookup}),
                'display': format_html(f'{title}({count})')
            }


class SCMFlagsFilter(SimpleListFilter):
    title = 'SCM Flags'
    parameter_name = 'status_id'

    def lookups(self, request, model_admin):
        children = SystemStatus.objects.filter(
            system_code='system_status_task_status_scm').first().get_children()
        # Return a list of tuples (value, display) for the filter options
        return [(str(child.id), child.name) for child in children]

    def queryset(self, request, queryset):
        value = self.value()
        if value is not None:
            # Filter the queryset based on the selected child node
            return queryset.filter(status_id=value)

    def choices(self, changelist):
        # Override choices to display the count for each child node
        for lookup, title in self.lookup_choices:
            count = TaskActionList.objects.filter(status_id=lookup).count()
            url = reverse('admin:dashboard_taskactionlist_changelist') + f'?status_id={lookup}'
            yield {
                'selected': self.value() == lookup,
                'query_string': changelist.get_query_string({self.parameter_name: lookup}),
                'display': format_html(f'{title}({count})')
            }


# sdfsdf
class StatusFilter(SimpleListFilter):
    title = 'Status'  # or use _('country') for translated title
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        statuses = set([c.status for c in
                        model_admin.model.objects.order_by('status__system_code').distinct('status__system_code')])
        return [(c.id, c.name) for c in statuses]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status__id__exact=self.value(), end_time__isnull=True)


class CategoryFilter(SimpleListFilter):
    title = 'Category'  # or use _('country') for translated title
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        categories = set([c.category for c in model_admin.model.objects.filter(category__isnull=False).order_by(
            'category__system_code').distinct('category__system_code')])
        if categories is not None:
            return [(c.id, c.name) for c in categories]
        return None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category_id=self.value())


# sdfsdfsdf

class CityFilterOld(SimpleListFilter):
    title = 'City'  # or use _('country') for translated title
    parameter_name = 'project__city_id'

    def lookups(self, request, model_admin):
        cities = set([c.project.city for c in model_admin.model.objects.filter(project__city__isnull=False).order_by(
            'project__city__code').distinct('project__city__code')])
        if cities is not None:
            return [(c.id, c.name) for c in cities]
        return None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(project__city__id__exact=self.value())

class CityFilter(SimpleListFilter):
    title = 'City'
    parameter_name = 'project__city_id'

    def lookups(self, request, model_admin):
        queryset = model_admin.get_queryset(request).select_related('project__city')
        cities = queryset.values_list('project__city__id', 'project__city__name')
        unique_cities = set(cities)
        return [(city_id, city_name) for city_id, city_name in unique_cities if city_id]

    def queryset(self, request, queryset):
        city_id = self.value()
        if city_id:
            return queryset.filter(project__city_id=city_id)
        return queryset

class RegionFilter(SimpleListFilter):
    title = 'Region'
    parameter_name = 'project__region_id'

    def lookups(self, request, model_admin):
        queryset = model_admin.get_queryset(request).select_related('project__region')
        regions = queryset.values_list('project__region__id', 'project__region__name')
        unique_regions = set(regions)
        return [(region_id, region_name) for region_id, region_name in unique_regions if region_id]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(project__region_id=value)
        return queryset

class RegionFilterOld(SimpleListFilter):
    title = 'Region'  # or use _('country') for translated title
    parameter_name = 'project__region_id'

    def lookups(self, request, model_admin):
        regions = set([c.project.region for c in
                       model_admin.model.objects.filter(project__region__isnull=False).order_by(
                           'project__region__code').distinct('project__region__code')])
        if regions is not None:
            return [(c.id, c.name) for c in regions]
        return None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(project__region__id__exact=self.value())


class InspectionFilterOld(SimpleListFilter):
    title = 'Flag Type'  # or use _('country') for translated title
    parameter_name = 'status__parent_id'

    def lookups(self, request, model_admin):
        regions = set([c.status.parent for c in model_admin.model.objects.filter(status__parent__isnull=False).order_by(
            'status__parent__code').distinct('status__parent__code')])
        if regions is not None:
            return [(c.id, c.name) for c in regions]
        return None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status__parent__id=self.value())

class InspectionFilter(SimpleListFilter):
    title = 'Flag Type'
    parameter_name = 'status__parent_id'

    def lookups(self, request, model_admin):
        queryset = model_admin.get_queryset(request).select_related('status__parent')
        parent_statuses = queryset.values_list('status__parent__id', 'status__parent__name').distinct()
        unique_parent_statuses = set(parent_statuses)
        return [(parent_id, parent_name) for parent_id, parent_name in unique_parent_statuses if parent_id]

    def queryset(self, request, queryset):
        parent_id = self.value()
        if parent_id:
            return queryset.filter(status__parent_id=parent_id)
        return queryset
        
class MaterialFlagsFilter(SimpleListFilter):
    title = 'Material Flags'
    parameter_name = 'status__id'

    def lookups(self, request, model_admin):
        filters = {
            'status__isnull': False,
            'status__parent__system_code': "system_status_task_status_material"
        }
        filter_q = Q(**filters)
        queryset = model_admin.get_queryset(request).filter(filter_q).select_related('status')
        flags = queryset.values_list('status__id', 'status__name').distinct()
        unique_flags = set(flags)
        return [(flag_id, flag_name) for flag_id, flag_name in unique_flags if flag_id]

    def queryset(self, request, queryset):
        flag_id = self.value()
        if flag_id:
            return queryset.filter(status__id=flag_id)
        return queryset


class MaterialFlagsFilterOld(SimpleListFilter):
    title = 'Material Flags'  # or use _('country') for translated title
    parameter_name = 'mat_flag_id'

    def lookups(self, request, model_admin):
        filters = {}
        filters['status__isnull'] = False
        filters['status__parent__system_code'] = "system_status_task_status_material"
        filter_q = Q(**filters)
        flags = set([c.status for c in
                     model_admin.model.objects.filter(filter_q).order_by('status__code').distinct('status__code')])
        if flags is not None:
            return [(c.id, c.name) for c in flags]
        return None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status__id__exact=self.value())


class InspectionFlagsFilterOld(SimpleListFilter):
    title = 'Inspection Flags'  # or use _('country') for translated title
    parameter_name = 'ins_flag_id'

    def lookups(self, request, model_admin):
        filters = {}
        filters['status__isnull'] = False
        filters['status__parent__system_code'] = "system_status_task_status_inspection"
        filter_q = Q(**filters)
        flags = set([c.status for c in
                     model_admin.model.objects.filter(filter_q).order_by('status__code').distinct('status__code')])
        if flags is not None:
            return [(c.id, c.name) for c in flags]
        return None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status__id__exact=self.value())

class InspectionFlagsFilter(SimpleListFilter):
    title = 'Inspection Flags'
    parameter_name = 'status__id'

    def lookups(self, request, model_admin):
        filters = {
            'status__isnull': False,
            'status__parent__system_code': "system_status_task_status_inspection"
        }
        filter_q = Q(**filters)
        queryset = model_admin.get_queryset(request).filter(filter_q).select_related('status')
        flags = queryset.values_list('status__id', 'status__name').distinct()
        unique_flags = set(flags)
        return [(flag_id, flag_name) for flag_id, flag_name in unique_flags if flag_id]

    def queryset(self, request, queryset):
        flag_id = self.value()
        if flag_id:
            return queryset.filter(status__id=flag_id)
        return queryset


class HSEFlagsFilterOld(SimpleListFilter):
    title = 'HSE Flags'  # or use _('country') for translated title
    parameter_name = 'hse_flag_id'

    def lookups(self, request, model_admin):
        filters = {}
        filters['status__isnull'] = False
        filters['status__parent__system_code'] = "system_status_task_status_hse"
        filter_q = Q(**filters)
        flags = set([c.status for c in
                     model_admin.model.objects.filter(filter_q).order_by('status__code').distinct('status__code')])
        if flags is not None:
            return [(c.id, c.name) for c in flags]
        return None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status__id__exact=self.value())

class HSEFlagsFilter(SimpleListFilter):
    title = 'HSE Flags'
    parameter_name = 'status__id'

    def lookups(self, request, model_admin):
        filters = {
            'status__isnull': False,
            'status__parent__system_code': "system_status_task_status_hse"
        }
        filter_q = Q(**filters)
        queryset = model_admin.get_queryset(request).filter(filter_q).select_related('status')
        flags = queryset.values_list('status__id', 'status__name').distinct()
        unique_flags = set(flags)
        return [(flag_id, flag_name) for flag_id, flag_name in unique_flags if flag_id]

    def queryset(self, request, queryset):
        flag_id = self.value()
        if flag_id:
            return queryset.filter(status__id=flag_id)
        return queryset


class SCMFlagsFilterOld(SimpleListFilter):
    title = 'SCM Flags'  # or use _('country') for translated title
    parameter_name = 'scm_flag_id'

    def lookups(self, request, model_admin):
        filters = {}
        filters['status__isnull'] = False
        filters['status__parent__system_code'] = "system_status_task_status_scm"
        filter_q = Q(**filters)
        flags = set([c.status for c in
                     model_admin.model.objects.filter(filter_q).order_by('status__code').distinct('status__code')])
        if flags is not None:
            return [(c.id, c.name) for c in flags]
        return None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status__id__exact=self.value())


class SCMFlagsFilter(SimpleListFilter):
    title = 'SCM Flags'
    parameter_name = 'status__id'

    def lookups(self, request, model_admin):
        filters = {
            'status__isnull': False,
            'status__parent__system_code': "system_status_task_status_scm"
        }
        filter_q = Q(**filters)
        queryset = model_admin.get_queryset(request).filter(filter_q).select_related('status')
        flags = queryset.values_list('status__id', 'status__name').distinct()
        unique_flags = set(flags)
        return [(flag_id, flag_name) for flag_id, flag_name in unique_flags if flag_id]

    def queryset(self, request, queryset):
        flag_id = self.value()
        if flag_id:
            return queryset.filter(status__id=flag_id)
        return queryset

class GenInspFlagsFilterOld(SimpleListFilter):
    title = 'General Inspection Flags'  # or use _('country') for translated title
    parameter_name = 'gen_insp_flag_id'

    def lookups(self, request, model_admin):
        filters = {}
        filters['status__isnull'] = False
        filters['status__parent__system_code'] = "system_status_task_status_gen_insp"
        filter_q = Q(**filters)
        flags = set([c.status for c in
                     model_admin.model.objects.filter(filter_q).order_by('status__code').distinct('status__code')])
        if flags is not None:
            return [(c.id, c.name) for c in flags]
        return None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status__id__exact=self.value())

class GenInspFlagsFilter(SimpleListFilter):
    title = 'General Inspection Flags'
    parameter_name = 'status__id'

    def lookups(self, request, model_admin):
        filters = {
            'status__isnull': False,
            'status__parent__system_code': "system_status_task_status_gen_insp"
        }
        filter_q = Q(**filters)
        queryset = model_admin.get_queryset(request).filter(filter_q).select_related('status')
        flags = queryset.values_list('status__id', 'status__name').distinct()
        unique_flags = set(flags)
        return [(flag_id, flag_name) for flag_id, flag_name in unique_flags if flag_id]

    def queryset(self, request, queryset):
        flag_id = self.value()
        if flag_id:
            return queryset.filter(status__id=flag_id)
        return queryset



class DesignInspFlagsFilterOld(SimpleListFilter):
    title = 'Design Inspection Flags'  # or use _('country') for translated title
    parameter_name = 'design_insp_flag_id'

    def lookups(self, request, model_admin):
        filters = {}
        filters['status__isnull'] = False
        filters['status__parent__system_code'] = "system_status_task_status_design_insp"
        filter_q = Q(**filters)
        flags = set([c.status for c in
                     model_admin.model.objects.filter(filter_q).order_by('status__code').distinct('status__code')])
        if flags is not None:
            return [(c.id, c.name) for c in flags]
        return None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status__id__exact=self.value())

class DesignInspFlagsFilter(SimpleListFilter):
    title = 'Design Inspection Flags'
    parameter_name = 'status__id'

    def lookups(self, request, model_admin):
        filters = {
            'status__isnull': False,
            'status__parent__system_code': "system_status_task_status_design_insp"
        }
        filter_q = Q(**filters)
        queryset = model_admin.get_queryset(request).filter(filter_q).select_related('status')
        flags = queryset.values_list('status__id', 'status__name').distinct()
        unique_flags = set(flags)
        return [(flag_id, flag_name) for flag_id, flag_name in unique_flags if flag_id]

    def queryset(self, request, queryset):
        flag_id = self.value()
        if flag_id:
            return queryset.filter(status__id=flag_id)
        return queryset


class MonthListFilter(admin.SimpleListFilter):
    title = _('Month Wise Counter Stats')
    parameter_name = 'month_counter'

    def lookups(self, request, model_admin):
        # Access the queryset from the model admin
        queryset = model_admin.get_queryset(request)

        # Generate month names and their counts based on the queryset
        month_counts = model_admin.model.objects.filter(id__in=queryset.values_list('id', flat=True)).annotate(
            month=ExtractMonth('created_on')).values('month').annotate(count=Count('id', distinct=True))
        # Convert month number to month name
        month_names = {1: _('January'), 2: _('February'), 3: _('March'), 4: _('April'), 5: _('May'), 6: _('June'),
                       7: _('July'), 8: _('August'), 9: _('September'), 10: _('October'), 11: _('November'),
                       12: _('December')}

        # Generate the list of filter options with month names
        return [(month['month'], f"{month_names[month['month']]} ({month['count']})") for month in month_counts]

    def queryset(self, request, queryset):
        if self.value():
            # Filter queryset by selected month
            return queryset.filter(created_on__month=self.value())


class TaskListAdmin(admin.ModelAdmin):
    list_display_links = None
    list_per_page = 10
    list_max_show_all = 100000000000000000000000000
    change_list_template = 'task_action_templates/change_list.html'
    change_form_template = 'admin/change_form.html'
    list_display = ['ca_ref_no', 'get_flag', 'get_description', 'get_type_of_work', 'get_task_progress',
                    'progress_difference',
                    'get_contractor', 'get_created_on','obsn_latest_dad_w_comment',
                    'obsn_latest_dad_qa_comment', 'action_btns']
    ordering = ['-created_on']
    list_filter = (('created_on', DateRangeFilter), RegionFilter, CityFilter,TimeAgoFilter,PendingStatusFilter,MonthListFilter, InspectionFilter,
                   MaterialFlagsFilter, InspectionFlagsFilter, 'project__organization')
    search_fields = ['serial_number', 'project__reference_number', 'status__name', 'created_by__email',
                     'updated_by__email', 'task__name', 'status__parent__name']
    date_hierarchy = 'created_on'
    actions = ['mark_as_seen', generate_project_report_pdf]
    fields = ['description', 'status']

    def get_form(self, request, obj=None, **kwargs):
        self.request = request
        return super().get_form(request, obj, **kwargs)

    # Permission Based List Ammendment
    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        self.request = request
        if 'dashboard.change_taskactionlist' in request.user.get_group_permissions():
            if 'edit_flag' not in list_display:
                list_display.append('edit_flag', )
        else:
            if 'edit_flag' in list_display:
                list_display.remove('edit_flag')
        return list_display

    # Admin Action
    def mark_as_seen(self, request, queryset):
        queryset.update(
            is_seen=True,
            seen_by=request.user,
            seen_on=datetime.now()
        )

    mark_as_seen.short_description = "Mark selected records as seen"

    """ Calculated Fields """

    def progress_difference(self, obj):
        # Calculate the difference between progress_actual and progress_planned
        if obj.project.progress_planned:
            difference = obj.project.progress_actual - obj.project.progress_planned
            # Return the difference with a sign prefix
            return f"{'Lag' if difference < 0 else 'Lead'}:{abs(difference)}%"
        elif obj.project.progress_actual:
            return f"{'Lead'}:{abs(obj.project.progress_actual)}%"
        else:
            return "Update Project Progress"

    # Set the progress_difference method as a read-only field
    progress_difference.short_description = 'Lag/Lead'
    progress_difference.admin_order_field = 'project'

    def ca_ref_no(self, obj):
        return obj.project.reference_number

    ca_ref_no.short_description = 'CA REF#'

    def get_obj_end_time(self, obj):
        return obj.end_time
    get_obj_end_time.short_description = 'Completion Date'

    def get_flag(self, obj, inspection_id=None, flag_id=None):
        return mark_safe(
            '<i class="fa fa-flag" data-toggle="tooltip" data-placement="top" title="{inspection_type}" style="color:{flag_color};font-size:25px"></i>'.format(
                flag_color=obj.status.color, inspection_type=obj.status.parent.name))

        # get_flag.admin_order_field  = 'parent_project_taskactions'  #Allows column order sorting

    get_flag.short_description = 'Flags'  # Renames column head

    def flag_parent_type(self, obj):
        return obj.status.parent.name

    flag_parent_type.short_description = 'INSPECTION TYPE'

    def type_of_work(self, obj):
        return obj.task

    type_of_work.short_description = 'TYPE OF WORK'

    def get_created_on(self, obj):
        return obj.created_on

    get_created_on.short_description = 'CREATED ON'

    def get_task_progress(self, obj):
        return f"{obj.project.progress_actual} %"

    get_task_progress.short_description = 'PROGRESS'

    def get_contractor(self, obj):
        if obj.project.contractor:
            return f"{obj.project.contractor}"
        return ""

    get_contractor.short_description = 'CONTRACTOR'

    def action_btns(self, obj):
        return mark_safe("<a href ='javascript:void(0);' onclick=ChatBoxApi.ShowChatBox('{task_action_id}','{project_ref_no}') class='btn-outline-info border-0 mr-2'><i class='far fa-comment-dots text-130'>\
        </i></a><a type='button' onclick=ChatBoxApi.task_action_first_attachment('{task_action_id}') class='btn-outline-info border-0'><i class='fas fa-paperclip text-130'></i></a>"
        .format(
            task_action_id=obj.id, project_ref_no=obj.project.reference_number.replace(' ', '_'),
            url=reverse('admin:dashboard_taskactionlist_change', args=[obj.pk])
        ))

    action_btns.short_description = 'ACTION'

    def edit_flag(self, obj):
        return mark_safe(
            "<div class='text-center'><a href={url} style='text-align:center;'><i class='fa fa-edit text-170'></i></a></div>".format(
                url=reverse('admin:dashboard_taskactionlist_change', args=[obj.pk])
            ))

    edit_flag.short_description = 'Edit Flag'

    def get_type_of_work(self, obj):
        if obj.project:
            return obj.project.name
        return ""

    get_type_of_work.short_description = 'Name Of Project'

    def get_obsn(self, obj):
        return mark_safe(
            '<a onclick="DashboardApi.obsnModal(\'{desc}\')" href="javascript:void(0);" class="btn btn-bold btn-outline-primary btn-h-primary fs--outline border-0 btn-a-primary radius-0 px-35 mb-1" data-toggle="tooltip" data-original-title="Flag Detail">Show Obsn</a>'.format(
                desc=str(obj.description),
            ))

    get_obsn.admin_order_field = 'Description'  # Allows column order sorting
    get_obsn.short_description = ''  # Renames column head

    def get_description(self, obj):
        if obj:
            if obj.is_seen:
                return mark_safe('<p>{obsn}</p>'.format(
                    obsn=str(obj.description)[0].upper() + str(obj.description)[1:],
                ))
            return mark_safe('<p class="font-weight-bold">{obsn}</p>'.format(
                obsn=str(obj.description)[0].upper() + str(obj.description)[1:],
            ))
        else:
            return ""

    get_description.short_description = 'Obsn'  # Renames column head

    def get_is_seen(self, obj):
        if obj.is_seen:
            return mark_safe('<a onclick="DashboardApi.changeSeenStatus(\'{obj_id}\')" href="javascript:void(0);" data-toggle="tooltip" data-original-title="Flag Detail">\
                <input type="checkbox" class="ace-switch input-lg ace-switch-bars-h ace-switch-check ace-switch-times text-grey-l2 bgc-orange-d2 radius-2px" checked></a>'.format(
                obj_id=str(obj.id),
            ))
        else:
            return mark_safe('<a onclick="DashboardApi.changeSeenStatus(\'{obj_id}\')" href="javascript:void(0);" data-toggle="tooltip" data-original-title="Flag Detail">\
                <input type="checkbox" class="ace-switch input-lg ace-switch-bars-h ace-switch-check ace-switch-times text-grey-l2 bgc-orange-d2 radius-2px"></a>'.format(
                obj_id=str(obj.id),
            ))

    get_is_seen.admin_order_field = 'Is Seen'  # Allows column order sorting
    get_is_seen.short_description = 'Is Seen'  # Renames column head

    def edit_link(self, obj):
        tac_obj = TaskActionComment.objects.filter(task_action_id=obj.pk, ).first()
        if tac_obj:
            url = reverse('admin:dashboard_taskactioncommentlist_change', args=[tac_obj.pk])
            return format_html('<a style="font-weight:bold" href="{}">Edit Obsn</a>', url)
        else:
            return "No Obsn"

    edit_link.short_description = ''  # Renames column head

    def task_action_progress(self, obj):
        return obj.project.progress_actual  # replace with your calculation

    task_action_progress.admin_order_field = 'progress_actual'
    task_action_progress.short_description = 'Progress'

    def obsn_latest_dad_w_comment(self, obj):
        latest_comment = obj.project_taskactioncomment_related.all().filter(
            created_by__type__code__contains='dad_w').latest('created_on')
        if latest_comment:
            return latest_comment.description
        return "--------"

    obsn_latest_dad_w_comment.short_description = 'DAD-W Comments'

    def obsn_latest_dad_qa_comment(self, obj):
        latest_comment = obj.project_taskactioncomment_related.all().filter(
            created_by__type__code__contains='dad_qa').latest('created_on')
        if latest_comment:
            return latest_comment.description
        return "--------"

    obsn_latest_dad_qa_comment.short_description = 'DAD-QA Comments'

    def obsn_latest_comment(self, obj):
        comment = obj.project_taskactioncomment_related.all().filter(tag_to__isnull=True).order_by(
            "-created_on").first()
        if comment:
            return comment.description
        return ""

    obsn_latest_comment.admin_order_field = 'Obsn Status'
    obsn_latest_comment.short_description = 'Obsn Status'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'status':
            kwargs["queryset"] = SystemStatus.objects.filter(
                parent__system_code__in=['system_status_task_status_material',
                                         'system_status_task_status_inspection']).exclude(
                system_code__in=['system_status_task_status_material_green',
                                 'system_status_task_status_inspection_green'])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            # CS Admin
            re_path(r'^change_seen_status/$', self.change_seen_status, name='change_seen_status'),
        ]
        return my_urls + urls

    @csrf_exempt
    def change_seen_status(self, request):
        if request.method == 'POST':
            id = request.POST.get("task_action_id", None)
            task_action = TaskAction.objects.filter(id=id).first()
            if task_action:
                task_action.is_seen = True
                task_action.save()
            return redirect(reverse("admin:dashboard_taskactionlist_changelist"))
        return redirect(reverse("admin:dashboard_taskactionlist_changelist"))

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request, extra_context=extra_context)
        try:
            task_action_manager = TaskActionManager(TaskAction, request)
            queryset = response.context_data['cl'].queryset

        except (AttributeError, KeyError):
            return response
        
        self.request = request
        extra_context = extra_context or {}

        extra_context['inspection_flag_stats'] = task_action_manager.get_inspection_flags_stats()
        extra_context['material_flag_stats'] = task_action_manager.get_material_flags_stats()
        extra_context['selected_filters'] = self.selectedFilter(request)
        #extra_context['total_projects'] = Project.objects.filter().count()
        extra_context['total_projects'] = filtered_project_qs_rolebased_android(request).count()
        extra_context['queryset_count'] = queryset.count()
         # Timesince Select Filter
        extra_context['time_since_filter_form'] = TimeSinceFilterForm() 
        extra_context['flag_filter_form'] = FlagFilterForm(request=request) 
        return super().changelist_view(request, extra_context=extra_context)

    def response_change(self, request, obj):
        """
        Determine the response after an object has been successfully changed.
        If the object is on a paginated change list page, redirect back to that page.
        """
        response = super().response_change(request, obj)
        if request.GET.get('p'):
            page_num = int(request.GET['p'])
            if (page_num - 1) * self.list_per_page < self.get_queryset(request).count():
                # Calculate the index of the last object on the current page
                last_on_page = page_num * self.list_per_page - 1
                qs = self.get_queryset(request)
                obj_index = qs.order_by(self.model._meta.pk.name).index(obj)
                if obj_index > last_on_page:
                    # Object is on a later page, so redirect to the last page
                    last_page = (qs.count() - 1) // self.list_per_page + 1
                    query_string = request.GET.urlencode()
                    response['Location'] += f"&p={last_page}&{query_string}"
                else:
                    # Object is on the current page, so redirect back to it
                    response['Location'] += f"&p={page_num}"
        return response

    # Selected Filter Helper  Function
    def selectedFilter(self, request):
        formatted_string = ""
        if 'flag_id' in request.GET:
            flag_id = request.GET.get('flag_id', None)
            task_status = TaskStatus.objects.filter(id=flag_id).first()
            formatted_string = formatted_string + str(task_status.parent.name) + "-" + str(task_status.name) + " /"

        if 'project__city_id' in request.GET:
            city_id = request.GET.get('project__city_id', None)
            city = City.objects.filter(id=city_id).first()
            formatted_string = formatted_string + str(city.region.name) + "-" + str(city.name) + "/"

        if 'project__region_id' in request.GET:
            region_id = request.GET.get('project__region_id', None)
            region = Region.objects.filter(id=region_id).first()
            formatted_string = formatted_string + str(region.name) + "/"

        if 'status__parent_id' in request.GET:
            status_parent_id = request.GET.get('status__parent_id', None)
            status_parent = SystemStatus.objects.filter(parent_id=status_parent_id).first()
            formatted_string = formatted_string + str(status_parent.parent.name) + "/"

        if 'status_id' in request.GET:
            status_id = request.GET.get('status_id', None)
            status = SystemStatus.objects.filter(id=status_id).first()
            formatted_string = formatted_string + str(status.name) + "/"

        if 'drf__created_on__gte' and 'drf__created_on__lte' in request.GET.keys():
            drf__created_on__gte = request.GET.get('drf__created_on__gte', None)
            drf__created_on__lte = request.GET.get('drf__created_on__lte', None)
            formatted_string = formatted_string + str(drf__created_on__gte) + "  To  " + str(drf__created_on__lte) + "/"

        if 'project__organization__id__exact' in request.GET:
            organization_id = request.GET.get('project__organization__id__exact', None)
            organization = Organization.objects.get(id=organization_id)
            formatted_string = formatted_string + str(organization.name) + "/"

        return formatted_string

    def getFlagStats(self, flag_qs, flag_type=None):
        print(flag_qs.count())
        data_list = []
        if flag_type == "inspection":
            flags = SystemStatus.objects.filter(parent__system_code="system_status_task_status_inspection")
        else:
            flags = SystemStatus.objects.filter(parent__system_code="system_status_task_status_material")
        for entry in flags:
            entry_list = []
            entry_list.append(entry.color)
            entry_list.append(flag_qs.filter(status_id=str(entry.id)).count())
            entry_list.append(flag_qs.filter(parent__status_id=entry.id).count())
            data_list.append(entry_list)
        return data_list

    def get_queryset(self, request):
        task_action_manager = TaskActionManager(TaskAction, request)
        qs = task_action_manager.get_pending_flags()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs.order_by('-created_on')

        # Filter your queryset and use distinct() to get unique instances based on the primary key
        # qs = qs.filter(
        #     end_time__isnull=True,
        #     parent__isnull=True,
        #     project_taskfiles__isnull=False
        # ).exclude(
        #     Q(status__system_code='system_status_task_status_material_green') |
        #     Q(status__system_code='system_status_task_status_inspection_green')
        # ).order_by('-created_on').select_related('project_taskfiles').distinct('pk')

        # Get unique task_action_id values from TaskFile
        # unique_task_action_ids = TaskFile.objects.values('task_action_id').distinct()
        # # Start with a base queryset
        # qs = qs.filter(
        #     id__in = unique_task_action_ids,
        #     end_time__isnull=True,
        # ).exclude(
        #     Q(status__system_code='system_status_task_status_material_green') |
        #     Q(status__system_code='system_status_task_status_inspection_green')
        # ).order_by('-created_on')
        return qs.filter(end_time__isnull=True, parent__isnull=True).exclude(
            status__system_code__contains='green').order_by('-created_on')

        # return qs.exclude(status__system_code__in=['system_status_task_status_material_green','system_status_task_status_inspection_green']).filter(end_time__isnull=True,parent__isnull=True,project_taskfiles__isnull=False).order_by('-created_on').distinct()

    def has_delete_permission(self, request, obj=None):
        if 'dashboard.can_delete_flag' in request.user.get_group_permissions():
            return True
        else:
            return False

    def has_add_permission(self, request):
        return False

    # def has_change_permission(self, request, obj=None):
    #     if 'dashboard.change_taskactionlist' in request.user.get_group_permissions():
    #         if 'edit_flag' not in self.list_display:
    #             self.list_display.append('edit_flag')
    #         return True
    #     # if request.user.is_superuser == 0:
    #     #     return True
    #     else:
    #         if 'edit_flag' in self.list_display:
    #             self.list_display.remove('edit_flag')
    #         return False

    def has_view_permission(self, request, obj=None):
        if 'dashboard.view_taskactionlist' in request.user.get_group_permissions():
            return True
        else:
            return False

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            # Only set added_by during the first save.
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        obj.ip = get_client_ip(request)

        # Updating Task Action Comments
        task_action_comment = TaskActionComment.objects.filter(task_action_id=obj.id).first()
        task_action_comment.description = obj.description
        task_action_comment.save()

        super().save_model(request, obj, form, change)


admin.site.register(TaskActionList, TaskListAdmin)
