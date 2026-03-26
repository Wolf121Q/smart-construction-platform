import jwt
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from project.api.login.utils import generate_refresh_token,generate_access_token,generate_base64_uid
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from core.models import User
from datetime import datetime


@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login_view(request):
    try:
        with open('/tmp/login_check_RAY.txt', 'a') as f:
            f.write(f"🧨 Login view HIT at {datetime.now()}\n")
    except Exception as e:
        # Optional: log this to another file if debugging file writing
        with open('/tmp/login_errors.txt', 'a') as ef:
            ef.write(f"❌ Error writing login_check_RAY.txt: {e}\n")


    response = Response()
    response.data = {'status':0,'message':'','access_token':None}
    username = request.data.get('username')
    password = request.data.get('password')
    device_token = request.data.get('device_token',None)
    device_uuid = request.data.get('device_uuid',None)

    if (username is None) or (password is None):
        #raise exceptions.AuthenticationFailed('username and password required')
        response.data = {'status': 0, 'message': 'username and password required','access_token':None}
        return response

    user = User.objects.filter(username=username).first()

    if(user is None):
        response.data = {'status': 0, 'message': 'Wrong User','access_token':None}
        return response

    if (user.is_active == 0):
        response.data = {'status': 0, 'message': 'User is inactive','access_token':None}
        return response

    if (user.is_mobile_user == 0):
        response.data = {'status': 0, 'message': 'User is not Allowed','access_token':None}
        return response
        #raise exceptions.AuthenticationFailed('user not found')
    if (not user.check_password(password)):
        response.data = {'status': 0, 'message': 'Wrong Password','access_token':None}
        return response
        #raise exceptions.AuthenticationFailed('wrong password')

    if device_uuid is not None and device_token is not None:
        user.device_uuid = device_uuid
        user.device_token = device_token
        user.save()

    #avatar_encode = ""
    # if user.avatar is not None and user.avatar:
    #     avatar_encode = base64.b64encode(user.avatar.read())
    #user_info = {'serial_number':user.serial_number,'username':user.username,'email':user.email,'first_name':user.first_name,'last_name':user.last_name,'avatar':avatar_encode}

    #serialized_user = UserSerializer(user).data
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)


    #print('ACCESS= ' + access_token + 'REFRESH=' + refresh_token)
    # response.data = {
    #     'api_token': access_token,
    #     #'refresh': refresh_token,
    #     #'user': serialized_user,
    # }
    response.data = {'status': 1, 'message': 'User Login Successful','user name':user.full_name,'access_token':access_token}
    return response

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_protect
def refresh_token_view(request):

    response = Response()
    response.data = {'status':0,'message':'','data':{'access_token': None,'refresh_token':None}}

    '''
    To obtain a new access_token this view expects 2 important things:
        1. a cookie that contains a valid refresh_token
        2. a header 'X-CSRFTOKEN' with a valid csrf token, client app can get it from cookies "csrftoken"
    '''
    refresh_token = request.COOKIES.get('refreshtoken')
    if refresh_token is None:
        response.data = {'status': 0, 'message': 'Authentication credentials were not provided', 'data': {'access_token': None, 'refresh_token': None}}
        # raise exceptions.AuthenticationFailed(
        #     'Authentication credentials were not provided.')
    try:
        payload = jwt.decode(
            refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        response.data = {'status': 0, 'message': 'Expired refresh token, please login again','data': {'access_token': None, 'refresh_token': None}}
        # raise exceptions.AuthenticationFailed(
        #     'expired refresh token, please login again.')

    user = User.objects.filter(id=generate_base64_uid(payload.get('user_id'))).first()
    if user is None:
        #raise exceptions.AuthenticationFailed('User not found')
        response.data = {'status': 0, 'message': 'User not found','data': {'access_token': None, 'refresh_token': None}}
    if not user.is_active:
        #raise exceptions.AuthenticationFailed('user is inactive')
        response.data = {'status': 0, 'message': 'User is inactive','data': {'access_token': None, 'refresh_token': None}}


    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    response.data = {'status': 1, 'message': 'access_token', 'data': {'access_token': access_token, 'refresh_token': refresh_token}}
    return response
    #return Response({'access_token': access_token})


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_protect
def logout_view(request):
    response = Response()
    response.data = {'status':0,'message':'','data':{'access_token': None,'refresh_token':None}}

    # Post is for logging out in current browser
    try:
        refresh_token = request.data["refresh_token"]

        token = OutstandingToken.objects.get(token=refresh_token)
        return Response({'access_token': token.user.first_name})

    #     if token.user == request.user:
    #         BlacklistedToken.objects.create(token=token)
    #     return Response(status=status.HTTP_205_RESET_CONTENT)
    except:
        response.data = {'status': 0, 'message': str(status.HTTP_400_BAD_REQUEST), 'data': {'access_token': None, 'refresh_token': None}}
        return response
        #return Response(status=status.HTTP_400_BAD_REQUEST)