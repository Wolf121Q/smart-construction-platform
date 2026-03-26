#https://itecnote.com/tecnote/python-pass-a-custom-queryset-to-serializer-in-django-rest-framework/
#https://stackoverflow.com/questions/47763185/how-to-serialize-a-django-mptt-family-and-keep-it-hierarchical
from rest_framework import serializers
from core.models import User

class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ['serial_number','full_name','email','username','last_activity','user_avatar_raw']
        #fields = '__all__'

