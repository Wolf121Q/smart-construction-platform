from django.urls import path
from .views import getFlags,login_view,refresh_token_view,logout_view,UpdateProjectProgressView,getFlagAttachments,getStatuses,getTypes,getUserAssociatedFlags,getOrganizations,getProjects,getCities,getRegions,getProjectTasks,UpdateProjectTasks,UpdateProjectTasksProgress,UpdateAvatar,ChangePassword,UserProfile,getAppVersion
urlpatterns = [
    path('statuses', getStatuses, name='statuses'),
    path('types', getTypes, name='types'),
    path('organizations', getOrganizations, name='organizations'),
    path('projects', getProjects, name='projects'),
    path('regions', getRegions, name='regions'),
    path('getappversion', getAppVersion, name='app_versions'),
    path('cities', getCities, name='cities'),
    path('project_tasks', getProjectTasks, name='project_tasks'),
    path('get_flag_stats', getUserAssociatedFlags, name='get_flag_stats'),
    path('project_flags', getFlags, name='project_flags'),
    path('project_flag_attachments', getFlagAttachments, name='project_flag_attachments'),
    path('update_tasks', UpdateProjectTasks, name='update_tasks'),
    path('update_tasks_progress', UpdateProjectTasksProgress, name='update_tasks_progress'),
    path('update_project_progress', UpdateProjectProgressView, name='update_project_progress'),
    path('user_profile', UserProfile, name='user_profile'),
    path('update_avatar', UpdateAvatar, name='update_avatar'),
    path('change_password', ChangePassword, name='change_password'),
    path('login', login_view, name='login'),
    path('refresh', refresh_token_view, name='refresh'),
    path('logout', logout_view, name='logout'),
]