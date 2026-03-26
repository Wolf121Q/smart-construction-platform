from django.contrib.admin.apps import AdminConfig

class AppAdminConfig(AdminConfig):
    default_site = 'ConstructionManagementSystem.admin.AppAdminSite'
    label = "admin"