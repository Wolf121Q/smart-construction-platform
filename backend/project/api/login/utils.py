import datetime
import jwt
from django.conf import settings
import base64
import uuid

def generate_uid_base64(uuid):
    # uuid to b64 string and back
    uuid_to_b64str = base64.urlsafe_b64encode(uuid.bytes).decode('utf8').rstrip('=\n')
    #b64str_to_uuid = uuid.UUID(bytes=base64.urlsafe_b64decode(f'{uuid_to_b64str}=='))
    return uuid_to_b64str

def generate_base64_uid(uuid_to_b64str):
    # uuid to b64 string and back
    #uuid_to_b64str = base64.urlsafe_b64encode(uuid.uuid1().bytes).decode('utf8').rstrip('=\n')
    b64str_to_uuid = uuid.UUID(bytes=base64.urlsafe_b64decode(f'{uuid_to_b64str}=='))
    return b64str_to_uuid


def generate_access_token(user):
    access_token_payload = {
        'user_id': generate_uid_base64(user.id),
        #'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, minutes=5),
        'iat': datetime.datetime.utcnow(),
    }
    #access_token = jwt.encode(access_token_payload,settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
    print()
    access_token = jwt.encode(access_token_payload,settings.SECRET_KEY, algorithm='HS256')
    return access_token


def generate_refresh_token(user):
  
    refresh_token_payload = {
        'user_id': generate_uid_base64(user.id),
        #'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    #refresh_token = jwt.encode(refresh_token_payload, settings.REFRESH_TOKEN_SECRET, algorithm='HS256').decode('utf-8')
    refresh_token = jwt.encode(refresh_token_payload, settings.REFRESH_TOKEN_SECRET, algorithm='HS256')

    return refresh_token