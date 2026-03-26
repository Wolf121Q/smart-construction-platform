import jwt
from rest_framework.authentication import BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework.response import Response
from rest_framework import exceptions
from django.conf import settings
#from django.contrib.auth import get_user_model
from core.models import User
from .utils import generate_base64_uid

class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        # Return the failure reason instead of an HttpResponse
        return reason


class SafeJWTAuthentication(BaseAuthentication):
    '''
        custom authentication utils for DRF and JWT
        https://github.com/encode/django-rest-framework/blob/master/rest_framework/authentication.py
    '''

    def authenticate(self, request):
        response = Response()
        response.data = {'status': -1, 'message': '', 'response_data': None}
        #User = get_user_model()
        authorization_heaader = request.headers.get('Authorization')

        if not authorization_heaader:
            return None
        try:
            # header = 'Token xxxxxxxxxxxxxxxxxxxxxxxx'
            access_token = authorization_heaader.split(' ')[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
            #response.data = {'status': -1, 'message': 'Access_token expired', 'response_data': None}
            #return response
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')
            #response.data = {'status': -1, 'message': 'Token prefix missing', 'response_data': None}
            #return response

        user = User.objects.filter(id=generate_base64_uid(payload['user_id'])).first()
        #user = User.objects.filter(id=payload['user_id']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
            #response.data = {'status': -1, 'message': 'User not found', 'response_data': None}
            #return response

        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')
            #response.data = {'status': -1, 'message': 'User is inactive', 'response_data': None}
            #return response

        #self.enforce_csrf(request)
        return (user, None)

    def enforce_csrf(self, request):
        """
        Enforce CSRF validation
        """
        check = CSRFCheck()
        # populates request.META['CSRF_COOKIE'], which is used in process_view()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        #print(reason)
        if reason:
            # CSRF failed, bail with explicit error message
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)
