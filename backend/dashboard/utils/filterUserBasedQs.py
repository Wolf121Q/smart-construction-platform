from django.db.models import Q
from organization.models import Region,City,Organization
from project.models import TaskAction,Project
from datetime import datetime, timedelta
from django.db.models import Subquery
from itertools import islice, chain
from django.db.models import Count

def filtered_qs_rolebased(request,qs=None):
    project_qs_filter = Project.objects.filter(name='')
    qs = Project.objects.filter()
    user_group_name = request.user.groups.values_list('id',flat = True) 
    user_group_name_as_list = list(user_group_name)

    region_qs = qs.filter(Q(region__groups__id__in = user_group_name_as_list) | Q(region__users__id = request.user.id))
    if region_qs:
        project_qs_filter = region_qs

    city_qs = qs.filter(Q(city__groups__id__in = user_group_name_as_list) | Q(city__users__id = request.user.id))
    if city_qs:
        project_qs_filter = project_qs_filter.union(city_qs)    

    organization_qs = qs.filter(Q(organization__groups__id__in = user_group_name_as_list) | Q(organization__users__id = request.user.id))
    if organization_qs:
        project_qs_filter = project_qs_filter.union(organization_qs)    
    
    project_qs = qs.filter(Q(groups__id__in = user_group_name_as_list) | Q(users__id = request.user.id))
    if project_qs:
        project_qs_filter = project_qs_filter.union(project_qs)    

    if project_qs_filter:
        return list(project_qs_filter.values_list('id',flat=True))
    else:
        return qs

def filtered_project_qs_rolebased_android(request):
    user_group_id = request.user.groups.values_list('id',flat = True) 
    user_group_id_as_list = list(user_group_id)

    """ REGIONS-CITIES-ORGANIZATIONS IN WHICH CONTAINS GROUP OR USER RELATED TO CURRENT USER """
    regions = Region.objects.filter(Q(groups__id__in = user_group_id_as_list) | Q(users__id = request.user.id))
    cities = City.objects.filter(Q(groups__id__in = user_group_id_as_list) | Q(users__id = request.user.id))
    organizations = Organization.objects.filter(Q(groups__id__in = user_group_id_as_list) | Q(users__id = request.user.id))

    """ FILTERING PROJECTS BASED ON REGIONS-CITIES-ORGANIZATIONS """
    # Query projects based on group or user associations
    project_qs = Project.objects.filter(
        Q(groups__id__in=user_group_id_as_list) | Q(users__id=request.user.id) |
        Q(region_id__in=Subquery(regions.values('id'))) |
        Q(city_id__in=Subquery(cities.values('id'))) |
        Q(organization_id__in=Subquery(organizations.values('id')))
    ).distinct()

    return project_qs

def filtered_region_rolebased_android(request):
    project_qs = filtered_project_qs_rolebased_android(request)
    regions = Region.objects.filter(id__in = Subquery(project_qs.values('region_id')),status = 'active').order_by("ordering")
    return regions

def filtered_region_rolebased(request,qs):
    if qs:     
        filtered_regions =  set([c.region for c in qs.order_by('region__code').distinct('region__code')])
        return [c.id for c in filtered_regions]
    return []

def filtered_city_rolebased(request,qs):
    if qs:     
        cities =  set([c.city for c in qs.order_by('city__code').distinct('city__code')])
        return [c.id for c in cities]
    return []
        
    # if request.user:
    #     return request.user

 
# Weekly Obsns Helper Functions
def weekly_obsns_datefilter(request,task_action_qs):
    if 'drf__created_on__gte' and 'drf__created_on__lte' in request.GET.keys():
        task_action_qs = task_action_qs.filter(created_on__date__gte=(datetime.strptime(request.GET['drf__created_on__gte'], '%Y-%m-%d') + timedelta(days=0)),created_on__lte= (datetime.strptime(request.GET['drf__created_on__lte'], '%Y-%m-%d') + timedelta(days=0)))
    else:
        # task_action_qs = task_action_qs.filter(created_on__date__gte = str((datetime.now()-timedelta(days=7)).date()))
        return task_action_qs

    if task_action_qs:
        return task_action_qs
    else:
        return TaskAction.objects.none()     
 