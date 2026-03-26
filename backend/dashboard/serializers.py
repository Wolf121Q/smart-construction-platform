from rest_framework import serializers
from core.models import User
from project.models import Project,Task,TaskAction,TaskActionComment,TaskFile


# USER SERIALIZER
class UserSerializer(serializers.ModelSerializer):
    value = serializers.ReadOnlyField(source='id')
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        if obj.middle_name:
            return str(obj.first_name) + " " + str(obj.middle_name) + " " + str(obj.last_name) + " (" + str(obj.type.name)+")"
        else:
            return str(obj.first_name) + " " + str(obj.last_name)+ " (" + str(obj.type.name)+")"

    class Meta:
        model = User
        fields = ['value','full_name']

class ProjectSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField(source='status.name')
    category = serializers.ReadOnlyField(source='category.name')
    region = serializers.ReadOnlyField(source='region.name')
    city = serializers.ReadOnlyField(source='city.name')
    organization = serializers.ReadOnlyField(source='organization.name')

    class Meta:
        model = Project
        fields = ['id','project_name','code','status','category','region','city','organization','created_on']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id','name','code','start_date','end_date','created_on']

class TaskActionSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    task    = TaskSerializer()
    class Meta:
        model = TaskAction
        fields = ['id','start_time','end_time','duration','latitude','longitude','created_on','project','task']

class TaskActionCommentSerializer(serializers.ModelSerializer):
    description = serializers.ReadOnlyField(source='description.html')
    class Meta:
        model = TaskActionComment
        fields = ['id','serial_number','description','created_on','latitude','longitude','created_on']

class TaskFileSerializer(serializers.ModelSerializer):
    task_action_comment = TaskActionCommentSerializer()
    class Meta:
        model = TaskFile
        fields = ['id','attachment','task_action_comment']