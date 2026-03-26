from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework import status
from utils.IP import get_client_ip
import base64
from project.api.login.authentication import SafeJWTAuthentication
from project.api.login.serializers import UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
@authentication_classes([SafeJWTAuthentication, ])
#@authentication_classes([SafeJWTAuthentication,])
def UserProfile(request):
    response = Response(content_type= 'application/json')
    response.data = {'status':0,'message':'Method is not allowed','data':{None}}
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            serialized_user = UserSerializer(user).data
            response.data = {'status': 1, 'message': 'User Profile', 'response_data': serialized_user}
            return response
        else:
            response.data = {'status': 0, 'message': '', 'response_data': None}
    return response



@api_view(['POST'])
@permission_classes([AllowAny])
# @csrf_protect
@csrf_exempt
@authentication_classes([SafeJWTAuthentication, ])
def UpdateAvatar(request):
    response = Response()
    response.data = {'status':0,'message':'Method is not allowed','response_data':{None}}
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            if request.FILES['avatar']:
                user.avatar = request.FILES['avatar']
                user.ip = get_client_ip(request)
                user.save()
                avatar_encode = ""

                response.data = {'status': 1, 'message': 'Avatar Updated successfully','response_data': None}
                return response

            response.data = {'status': 2, 'message': 'Avatar is incorrect','response_data': {None}}
            return response
        response.data = {'status': -1, 'message': 'user is not authenticated','response_data': None}
    return response


@api_view(['POST'])
@permission_classes([AllowAny])
# @csrf_protect
@csrf_exempt
@authentication_classes([SafeJWTAuthentication, ])
def ChangePassword(request):
    response = Response()
    response.data = {'status': 0, 'message': 'Method is not allowed', 'response_data': {None}}
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            if request.POST.get('old_password', None):
                if not user.check_password(request.POST.get('old_password')):
                    response.data = {'status': 0, 'message': 'The old password you have entered is incorrect','response_data': {None}}

                elif request.POST.get('new_password', None) and request.POST.get('confirm_password', None):
                    user.set_password(request.POST.get('new_password', None))
                    user.ip = get_client_ip(request)
                    user.save()
                    response.data = {'status': 1, 'message': 'Password updated successfully', 'response_data': {None}}
                else:
                    response.data = {'status': 0, 'message': 'The New password you have entered is incorrect','response_data': {None}}

    return response



