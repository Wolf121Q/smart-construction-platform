from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from dashboard.models import TaskActionList,Project
from core.models import SystemStatus
from django.utils.safestring import mark_safe
from daterange_filter.filter import DateRangeFilter
from project.models import TaskStatus,Region,City,TaskAction,TaskActionTimeLine,TaskActionComment,TaskFile,Organization
from django.shortcuts import redirect
from django.urls import re_path,reverse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.utils.html import format_html
from dashboard.utils.filterUserBasedQs import filtered_qs_rolebased
from utils.IP import get_client_ip
from dashboard.utils.generateRectifiedReport import generate_project_report_pdf
from django.db.models import Count,Q
from django.db.models.functions import TruncMonth
from django.utils.translation import gettext_lazy as _



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
        children = SystemStatus.objects.filter(system_code='system_status_task_status_inspection').first().get_children()
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
    title = 'Status' # or use _('country') for translated title
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        statuses = set([c.status for c in model_admin.model.objects.order_by('status__system_code').distinct('status__system_code')])
        return [(c.id, c.name) for c in statuses]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status__id__exact=self.value(),end_time__isnull = True)

class CategoryFilter(SimpleListFilter):
    title = 'Category' # or use _('country') for translated title
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        categories = set([c.category for c in model_admin.model.objects.filter(category__isnull=False).order_by('category__system_code').distinct('category__system_code')])
        if categories is not None:
            return [(c.id, c.name) for c in categories]
        return None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category_id = self.value())

# sdfsdfsdf

class CityFilter(SimpleListFilter):
    title = 'City' # or use _('country') for translated title
    parameter_name = 'project__city_id'

    def lookups(self, request, model_admin):
        cities = set([c.project.city for c in model_admin.model.objects.filter(project__city__isnull=False).order_by('project__city__code').distinct('project__city__code')])
        if cities is not None:
            return [(c.id, c.name) for c in cities]
        return None
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(project__city__id__exact=self.value())

class RegionFilter(SimpleListFilter):
    title = 'Region' # or use _('country') for translated title
    parameter_name = 'project__region_id'
  
    def lookups(self, request, model_admin):
        regions = set([c.project.region for c in model_admin.model.objects.filter(project__region__isnull=False).order_by('project__region__code').distinct('project__region__code')])
        if regions is not None:
            return [(c.id, c.name) for c in regions]
        return None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(project__region__id__exact=self.value())

class InspectionFilter(SimpleListFilter):
    title = 'Flag Type' # or use _('country') for translated title
    parameter_name = 'status__parent_id'

    def lookups(self, request, model_admin):
        regions = set([c.status.parent for c in model_admin.model.objects.filter(status__parent__isnull=False).order_by('status__parent__code').distinct('status__parent__code')])
        if regions is not None:
            return [(c.id, c.name) for c in regions]
        return None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status__parent__id = self.value())

class MaterialFlagsFilter(SimpleListFilter):
    title = 'Material Flags' # or use _('country') for translated title
    parameter_name = 'mat_flag_id'

    def lookups(self, request, model_admin):
        filters = {}
        filters['status__isnull'] = False
        filters['status__parent__system_code'] = "system_status_task_status_material"
        filter_q = Q(**filters)
        flags = set([c.status for c in model_admin.model.objects.filter(filter_q).order_by('status__code').distinct('status__code')])
        if flags is not None:
            return [(c.id, c.name) for c in flags]
        return None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status__id__exact = self.value(),end_time__isnull=True)

class InspectionFlagsFilter(SimpleListFilter):
    title = 'Inspection Flags' # or use _('country') for translated title
    parameter_name = 'ins_flag_id'

    def lookups(self, request, model_admin):
        filters = {}
        filters['status__isnull'] = False
        filters['status__parent__system_code'] = "system_status_task_status_inspection"
        filter_q = Q(**filters)
        flags = set([c.status for c in model_admin.model.objects.filter(filter_q).order_by('status__code').distinct('status__code')])
        if flags is not None:
            return [(c.id, c.name) for c in flags]
        return None

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status__id__exact = self.value(),end_time__isnull=True)


class MonthListFilter(admin.SimpleListFilter):
    title = _('Month')  # The title that will be displayed in the admin
    parameter_name = 'month'  # The URL parameter for the filter

    def lookups(self, request, model_admin):
        # Get a list of unique months in your queryset
        qs = model_admin.model._default_manager.get_queryset().filter(end_time__isnull=True,parent__isnull=True).exclude(status__system_code__in = ['system_status_task_status_material_green','system_status_task_status_inspection_green']).order_by('-created_on')

        print(qs.count())
        unique_months = qs.annotate(
            month=TruncMonth('created_on')
        ).values('month').annotate(count=Count('id')).order_by('-month')

        # Create lookup options based on the unique months, including count
        lookups = [
            (
                f"{month['month'].year}-{month['month'].month}",
                f"{month['month'].strftime('%B %Y')} ({month['count']})"
            ) for month in unique_months
        ]
        # Add an option for filtering by all months
        lookups.insert(0, ('all', _('All Months')))
        return lookups

    def queryset(self, request, queryset):
        if self.value() == 'all':
            return queryset
        
        elif self.value():
            # Filter the queryset based on the selected month
            return queryset.filter(created_on__year=int(self.value().split('-')[0]),created_on__month=int(self.value().split('-')[1]))

class TaskListAdmin(admin.ModelAdmin):
    list_display_links = None
    list_per_page = 10
    list_max_show_all = 100000000000000000000000000
    # change_list_template = 'task_action_templates/change_list.html'
    change_list_template = 'task_action_templates/change_list__2023.html'
    change_form_template = 'admin/change_form.html'
    list_display = ['ca_ref_no','get_flag','get_description','get_type_of_work','get_task_progress','get_contractor','get_created_on','obsn_latest_dad_w_comment','obsn_latest_dad_qa_comment','action_btns']
    ordering = ['-created_on']
    list_filter = (('created_on',DateRangeFilter),MonthListFilter,RegionFilter,CityFilter,InspectionFilter,MaterialFlagsFilter,InspectionFlagsFilter,'project__organization')
    search_fields = ['serial_number','project__reference_number','status__name','created_by__email','updated_by__email','task__name','status__parent__name']
    date_hierarchy = 'created_on'
    actions = ['mark_as_seen',generate_project_report_pdf]
    fields = ['description','status']
    
    def get_form(self, request, obj=None, **kwargs):
        self.request = request
        return super().get_form(request, obj, **kwargs)

    # Permission Based List Ammendment
    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        self.request = request
        if 'dashboard.change_taskactionlist' in request.user.get_group_permissions():
            if 'edit_flag' not in list_display:
                list_display.append('edit_flag',)
        else:
            if 'edit_flag' in list_display:
                list_display.remove('edit_flag')
        return list_display
    
    # Admin Action
    def mark_as_seen(self, request, queryset):
        queryset.update(
            is_seen=True,
            seen_by = request.user,
            seen_on = datetime.now()
        )
    mark_as_seen.short_description = "Mark selected records as seen"

    """ Calculated Fields """    
    def ca_ref_no(self, obj):
        return obj.project.reference_number

    ca_ref_no.short_description = 'CA REF#'

    def get_flag(self, obj,inspection_id = None,flag_id = None):
        return mark_safe('<i class="fa fa-flag" data-toggle="tooltip" data-placement="top" title="{inspection_type}" style="color:{flag_color};font-size:25px"></i>'.format(flag_color = obj.status.color,inspection_type = obj.status.parent.name))   
    
    # get_flag.admin_order_field  = 'parent_project_taskactions'  #Allows column order sorting
    get_flag.short_description = 'Flags'  #Renames column head

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
            task_action_id = obj.id,project_ref_no = obj.project.reference_number.replace(' ', '_'),
            url = reverse('admin:dashboard_taskactionlist_change', args=[obj.pk])
        ))
    action_btns.short_description = 'ACTION'

    def edit_flag(self, obj):
        return mark_safe("<div class='text-center'><a href={url} style='text-align:center;'><i class='fa fa-edit text-170'></i></a></div>".format(
                url = reverse('admin:dashboard_taskactionlist_change', args=[obj.pk])
            ))
    
    edit_flag.short_description = 'Edit Flag'
    
    def get_type_of_work(self, obj):
        if obj.project:
            return obj.project.name
        return ""
    get_type_of_work.short_description = 'Name Of Project'

    def get_obsn(self, obj):
        return mark_safe('<a onclick="DashboardApi.obsnModal(\'{desc}\')" href="javascript:void(0);" class="btn btn-bold btn-outline-primary btn-h-primary fs--outline border-0 btn-a-primary radius-0 px-35 mb-1" data-toggle="tooltip" data-original-title="Flag Detail">Show Obsn</a>'.format(
            desc = str(obj.description),
        ))
    get_obsn.admin_order_field  = 'Description'  #Allows column order sorting
    get_obsn.short_description = ''  #Renames column head

    def get_description(self, obj):
        if obj:
            if obj.is_seen:
                return mark_safe('<p>{obsn}</p>'.format(
                    obsn = str(obj.description)[0].upper() + str(obj.description)[1:],
                ))
            return mark_safe('<p class="font-weight-bold">{obsn}</p>'.format(
                obsn = str(obj.description)[0].upper() + str(obj.description)[1:],
            ))
        else:
            return ""
    get_description.short_description = 'Obsn'  #Renames column head
    
    def get_is_seen(self, obj):
        if obj.is_seen:
            return mark_safe('<a onclick="DashboardApi.changeSeenStatus(\'{obj_id}\')" href="javascript:void(0);" data-toggle="tooltip" data-original-title="Flag Detail">\
                <input type="checkbox" class="ace-switch input-lg ace-switch-bars-h ace-switch-check ace-switch-times text-grey-l2 bgc-orange-d2 radius-2px" checked></a>'.format(
                obj_id = str(obj.id),
            ))
        else:
            return mark_safe('<a onclick="DashboardApi.changeSeenStatus(\'{obj_id}\')" href="javascript:void(0);" data-toggle="tooltip" data-original-title="Flag Detail">\
                <input type="checkbox" class="ace-switch input-lg ace-switch-bars-h ace-switch-check ace-switch-times text-grey-l2 bgc-orange-d2 radius-2px"></a>'.format(
                obj_id = str(obj.id),
            ))
    get_is_seen.admin_order_field  = 'Is Seen'  #Allows column order sorting
    get_is_seen.short_description = 'Is Seen'  #Renames column head

    def edit_link(self, obj):
        tac_obj = TaskActionComment.objects.filter(task_action_id=obj.pk,).first()
        if tac_obj:
            url = reverse('admin:dashboard_taskactioncommentlist_change', args=[tac_obj.pk])
            return format_html('<a style="font-weight:bold" href="{}">Edit Obsn</a>', url)
        else:
            return "No Obsn"
    edit_link.short_description = ''  #Renames column head

    def task_action_progress(self, obj):
        return obj.project.progress_actual # replace with your calculation
    task_action_progress.admin_order_field = 'progress_actual'
    task_action_progress.short_description = 'Progress'

    def obsn_latest_dad_w_comment(self, obj):
        latest_comment = obj.project_taskactioncomment_related.all().filter(created_by__type__code__contains='dad_w').latest('created_on')
        if latest_comment:
            return latest_comment.description
        return "--------"
    obsn_latest_dad_w_comment.short_description = 'DAD-W Comments'
    
    def obsn_latest_dad_qa_comment(self, obj):
        latest_comment = obj.project_taskactioncomment_related.all().filter(created_by__type__code__contains='dad_qa').latest('created_on')
        if latest_comment:
            return latest_comment.description
        return "--------"
    obsn_latest_dad_qa_comment.short_description = 'DAD-QA Comments'
    
    def obsn_latest_comment(self, obj):
        comment = obj.project_taskactioncomment_related.all().filter(tag_to__isnull=True).order_by("-created_on").first()
        if comment:
            return comment.description
        return ""
    obsn_latest_comment.admin_order_field = 'Obsn Status'
    obsn_latest_comment.short_description = 'Obsn Status'
  
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'status':
            kwargs["queryset"] = SystemStatus.objects.filter(parent__system_code__in =['system_status_task_status_material','system_status_task_status_inspection']).exclude(system_code__in = ['system_status_task_status_material_green','system_status_task_status_inspection_green'])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            # CS Admin
            re_path(r'^change_seen_status/$', self.change_seen_status,name='change_seen_status'),
        ]
        return my_urls + urls
    
    @csrf_exempt
    def change_seen_status(self,request):
        if request.method == 'POST':
            id = request.POST.get("task_action_id",None)
            task_action = TaskAction.objects.filter(id = id).first()
            if task_action:
                task_action.is_seen = True
                task_action.save()
            return redirect(reverse("admin:dashboard_taskactionlist_changelist"))
        return redirect(reverse("admin:dashboard_taskactionlist_changelist"))
    
    def changelist_view(self, request, extra_context=None):
        queryset = TaskActionList.objects.all()

        insp_flag_filtered_query_set = queryset.filter(status__parent__system_code = "system_status_task_status_inspection")
        mat_flag_filtered_query_set = queryset.filter(status__parent__system_code = "system_status_task_status_material")
        extra_context = {
             'mat_flag_filtered_query_set': self.getFlagStats(mat_flag_filtered_query_set,"material"),
             'ins_flag_filtered_query_set': self.getFlagStats(insp_flag_filtered_query_set,"inspection"),
        }
        extra_context['selected_filters'] = self.selectedFilter(request)
        extra_context['total_projects'] = Project.objects.filter().count()

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
    def selectedFilter(self,request):
        formatted_string = ""
        if 'flag_id' in request.GET:
            flag_id = request.GET.get('flag_id',None)
            task_status = TaskStatus.objects.filter(id = flag_id).first()
            formatted_string = formatted_string + str(task_status.parent.name) + "-" + str(task_status.name) +" /"
        
        if 'project__city_id' in request.GET:
            city_id = request.GET.get('project__city_id',None)
            city = City.objects.filter(id = city_id).first()
            formatted_string = formatted_string + str(city.region.name) + "-" + str(city.name) + "/"

        if 'project__region_id' in request.GET:
            region_id = request.GET.get('project__region_id',None)
            region = Region.objects.filter(id = region_id).first()
            formatted_string = formatted_string + str(region.name) + "/"
        
        if 'status__parent_id' in request.GET:
            status_parent_id = request.GET.get('status__parent_id',None)
            status_parent = SystemStatus.objects.filter(parent_id = status_parent_id).first()
            formatted_string = formatted_string + str(status_parent.parent.name) + "/"
        
        if 'status_id' in request.GET:
            status_id = request.GET.get('status_id',None)
            status = SystemStatus.objects.filter(id = status_id).first()
            formatted_string = formatted_string + str(status.name) + "/"
        
        if 'drf__created_on__gte' and 'drf__created_on__lte' in request.GET.keys():
            drf__created_on__gte = request.GET.get('drf__created_on__gte',None)
            drf__created_on__lte = request.GET.get('drf__created_on__lte',None)
            formatted_string = formatted_string + str(drf__created_on__gte) + "  To  " + str(drf__created_on__lte) + "/"
        

        if 'project__organization__id__exact' in request.GET:
            organization_id = request.GET.get('project__organization__id__exact',None)
            organization = Organization.objects.get(id=organization_id)
            formatted_string = formatted_string + str(organization.name) + "/"

        return formatted_string
    
    def getFlagStats(self,flag_qs,flag_type=None):
        data_list = []
        if flag_type == "inspection":
            flags = SystemStatus.objects.filter(parent__system_code = "system_status_task_status_inspection")
        else:
            flags = SystemStatus.objects.filter(parent__system_code = "system_status_task_status_material")
        for entry in flags:
            entry_list = []
            entry_list.append(entry.color)
            entry_list.append(flag_qs.filter(status_id = str(entry.id)).count())
            entry_list.append(flag_qs.filter(status_id = entry.id,end_time__isnull = False).count())
            data_list.append(entry_list)
        return data_list
 
 
    
    def get_queryset(self, request):
        qs = self.model._default_manager.get_queryset().filter(project_id__in = filtered_qs_rolebased(request),end_time__isnull=True).order_by("-created_on")
        combined_queryset = self.model.objects.none()
        time_line_obj = TaskActionTimeLine.objects.filter(user_type = request.user.type).first()
        if time_line_obj:
            time_line = datetime.now() - time_line_obj.time_line
            if time_line_obj.flag_type.all().count() > 0:
                for type in time_line_obj.flag_type.all():
                    qs = qs.exclude(status__type__system_code = type.system_code)
                    combined_queryset = combined_queryset | self.model._default_manager.get_queryset().filter(status__type__system_code = type.system_code,created_on__date__lt = time_line.date(),)
                qs = qs | combined_queryset
                qs = qs.order_by("-created_on")
            else:
                qs = qs
        else:
            qs = qs
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        

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
        return qs.filter(end_time__isnull=True,parent__isnull=True).exclude(status__system_code__in = ['system_status_task_status_material_green','system_status_task_status_inspection_green']).order_by('-created_on')

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
        task_action_comment = TaskActionComment.objects.filter(task_action_id = obj.id).first()
        task_action_comment.description = obj.description
        task_action_comment.save()

        super().save_model(request, obj, form, change)
     
admin.site.register(TaskActionList,TaskListAdmin)
