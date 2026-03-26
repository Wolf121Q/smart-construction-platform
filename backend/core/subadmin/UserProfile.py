from django.contrib import admin
from utils.IP import get_client_ip
from core.models import UserProfile
from django import forms
from project.models import Project
from django.contrib.admin.widgets import FilteredSelectMultiple


class ProjectForm(forms.ModelForm):
    projects = forms.ModelMultipleChoiceField(
        queryset=Project.objects.all(),  # Adjust the queryset as needed
        required=False,  # Set as required or not based on your requirements
        widget=forms.SelectMultiple,  # Use SelectMultiple widget to display as a list
    )

    class Meta:
        model = UserProfile
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['projects'].queryset = Project.objects.all().filter(users=self.instance.user)
         # Set the initial value for 'projects' to the user's associated projects
        self.initial['projects'] = Project.objects.all().filter(users=self.instance.user)

class UserProfileAdmin(admin.ModelAdmin):
    form = ProjectForm
    list_display = ('user','calulated_user_type','region','city','created_on','created_by','updated_by','updated_on')
    fields = ['user','region','city','projects']
    ordering = ['-created_on']
    list_filter = ('region',)
    search_fields = ['user__username','region__name','city__name']
    date_hierarchy = 'created_on'

    def calulated_user_type(self, obj):
        # Calculate the discounted price
        return obj.user.type
    calulated_user_type.short_description = 'Designation'

    def get_queryset(self, request):
        qs = super(UserProfileAdmin, self).get_queryset(request)
        return qs

    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return True
    def has_add_permission(self, request):
         if request.user.type.code == "system_type_user_developer_admin":
             return True
         else:
             return False
    
    def has_change_permission(self, request, obj=None):
         if request.user.type.code == "system_type_user_developer_admin":
             return True
         else:
             return False
    
    def has_view_permission(self, request, obj=None):
         if request.user.type.code == "system_type_user_developer_admin":
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
        # Project Management
        # Get the previously associated projects
        previous_projects = Project.objects.filter(users=obj.user)
        # Save the user object
        super(UserProfileAdmin, self).save_model(request, obj, form, change)
        # Compare the previous projects with the selected projects in the form
        selected_projects = form.cleaned_data.get('projects')
        excluded_projects = previous_projects.exclude(id__in=selected_projects)

        # Remove the user from excluded projects
        for project in excluded_projects:
            project.users.remove(obj.user)
        super().save_model(request, obj, form, change)

admin.site.register(UserProfile, UserProfileAdmin)