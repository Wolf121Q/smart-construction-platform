#https://itecnote.com/tecnote/python-pass-a-custom-queryset-to-serializer-in-django-rest-framework/
#https://stackoverflow.com/questions/47763185/how-to-serialize-a-django-mptt-family-and-keep-it-hierarchical
from rest_framework import serializers
from core.models import SystemStatus,SystemType

class StatusSerializer(serializers.ModelSerializer):
    parent_system_code = serializers.SerializerMethodField()

    def get_parent_system_code(self, obj):
        if obj.parent is not None and obj.parent:
            return str(obj.parent.system_code)
        else:
            return ""

    class Meta:
        model = SystemStatus
        fields = ['id','name', 'parent_system_code','code','system_code','color','parent', 'lft','rght','tree_id','mptt_level','status']
        #fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    parent_system_code = serializers.SerializerMethodField()

    def get_parent_system_code(self, obj):
        if obj.parent is not None and obj.parent:
            return str(obj.parent.system_code)
        else:
            return ""

    class Meta:
        model = SystemType
        fields = ['id','name', 'parent_system_code','code','system_code','color','parent', 'lft','rght','tree_id','mptt_level','status']
