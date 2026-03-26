from django.apps import AppConfig

class DashboardConfig(AppConfig):
    name = 'dashboard'
    verbose_name = 'Dashboard'

from django.contrib.admin.apps import AdminConfig
class AppAdminConfig(AdminConfig):
    default_site = 'dashboard.adminsite.AppAdminSite'
    label = "admin"