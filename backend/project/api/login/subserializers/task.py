import base64
from os import path
from rest_framework import serializers
from organization.models import City,Region
from project.models import Task,Project,Organization,TaskAction,TaskActionComment,TaskFile

class OrganizationSerializer(serializers.ModelSerializer):
    region_name = serializers.ReadOnlyField(source='region.name')
    region_id = serializers.ReadOnlyField(source='region.id')
    city_name = serializers.ReadOnlyField(source='city.name')
    city_id = serializers.ReadOnlyField(source='city.id')
    type_name = serializers.ReadOnlyField(source='type.name')
    type_id = serializers.ReadOnlyField(source='type.id')

    class Meta:
        model = Organization
        fields = ['id','name', 'code','phone','status','region_name','region_id','city_name','city_id','type_name','type_id']

class ProjectSerializer(serializers.ModelSerializer):
    region_name = serializers.ReadOnlyField(source='region.name')
    region_id = serializers.ReadOnlyField(source='region.id')
    city_name = serializers.ReadOnlyField(source='city.name')
    city_id = serializers.ReadOnlyField(source='city.id')
    organization_id = serializers.ReadOnlyField(source='organization.id')
    #description = serializers.ReadOnlyField(source='description.html')
    organization = OrganizationSerializer(many=False, read_only=True)
    thumbnail = serializers.SerializerMethodField()
    task_actions = serializers.SerializerMethodField()
    task_comments = serializers.SerializerMethodField()

    def get_thumbnail(self, obj):
        if obj.thumbnail is not None and obj.thumbnail and path.exists(str(obj.thumbnail.path)):
            base64_encode = base64.b64encode(obj.thumbnail.read())
            return base64_encode
        else:
            return None

    def get_task_actions(self, obj):
        task_actions = TaskAction.objects.filter(project=obj,created_by=self.context['request'].user).order_by("-created_on")
        serialized_task_actions = TaskActionSerializer(task_actions, many=True).data
        return serialized_task_actions

    def get_task_comments(self, obj):
        task_action_comments = TaskActionComment.objects.filter(project=obj,created_by=self.context['request'].user)
        serialized_task_action_comments = TaskActionCommentSerializer(task_action_comments, many=True).data
        return serialized_task_action_comments
        

    class Meta:
        model = Project
        fields = ['id','serial_number', 'name','region_id','region_name','city_id','city_name','organization_id','code','project_label','description','status','organization','start_date','end_date','duration','progress_planned','progress_actual','consultant_name','thumbnail','task_actions','task_comments']
        #fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    #description = serializers.ReadOnlyField(source='description.html')
    class Meta:
        model = City
        # fields = ['id','serial_number']
        fields = '__all__'

class RegionSerializer(serializers.ModelSerializer):
    #description = serializers.ReadOnlyField(source='description.html')
    class Meta:
        model = Region
        # fields = ['id','serial_number']
        fields = '__all__'


class TaskActionSerializer(serializers.ModelSerializer):
    #description = serializers.ReadOnlyField(source='description.html')
    created_by_name = serializers.SerializerMethodField()
    def get_created_by_name(self, obj):
        return obj.created_by.full_name


    class Meta:
        model = TaskAction
        # fields = ['id','serial_number']
        fields = '__all__'

class TaskActionCommentSerializer(serializers.ModelSerializer):
    #description = serializers.ReadOnlyField(source='description.html')
    class Meta:
        model = TaskActionComment
        # fields = ['id','serial_number']
        fields = '__all__'

class TaskFileSerializer(serializers.ModelSerializer):


    attachment = serializers.SerializerMethodField()

    def get_attachment(self, obj):
        if obj.attachment is not None and obj.attachment and path.exists(str(obj.attachment.path)):
            base64_encode = base64.b64encode(obj.attachment.read())
            return base64_encode

        else:
            return None

    class Meta:
        model = TaskFile
        # fields = ['id','serial_number']
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    task_actions = serializers.SerializerMethodField()
    task_comments = serializers.SerializerMethodField()
    # task_comments = TaskActionCommentSerializer(many=True, read_only=True,source='project_taskactioncomment_related')

    def get_task_actions(self, obj):
        task_actions = TaskAction.objects.filter(task=obj,created_by=self.context['request'].user)
        serialized_task_actions = TaskActionSerializer(task_actions, many=True).data
        return serialized_task_actions

    def get_task_comments(self, obj):
        task_action_comments = TaskActionComment.objects.filter(task=obj,created_by=self.context['request'].user)
        serialized_task_action_comments = TaskActionCommentSerializer(task_action_comments, many=True).data
        return serialized_task_action_comments
    #task_files = TaskFileSerializer(many=True, read_only=True,source='project_taskfile_related')
    #description = serializers.ReadOnlyField(source='description.html')
    class Meta:
        model = Task
        #fields = ['project','task_actions','task_comments','task_files','id','serial_number', 'created_on','name','code','description', 'status','start_date','end_date','duration']
        fields = '__all__'



