#from requests_toolbelt import MultipartEncoder
from requests_toolbelt.multipart.encoder import MultipartEncoder
from django.utils.safestring import mark_safe
import requests
from urllib.parse import urljoin
import json
import os
from django.conf import settings
import json
from vendor_company.models import VendorCompany
from vendor_company.serializers import VendorCompanySerializer
from datetime import datetime
from django.db.models import Q


def isExists(url):
    if os.path.isfile(os.path.join(settings.BASE_DIR, url.lstrip('/'))):
        return 1
    else:
        return 0

def response_parser(response, present='dict'):
    """ Convert NVR results
    """
    if isinstance(response, (list,)):
        result = "".join(response)
    else:
        result = response.text

    if present == 'dict':
        if isinstance(response, (list,)):
            events = []
            for event in response:
                e = json.loads(json.dumps(xmltodict.parse(event)))
                events.append(e)
            return events
        return json.loads(json.dumps(xmltodict.parse(result)))
    else:
        return result

def checkKey(test_dict, key):
    value = test_dict[key]
    if value:
        return True
    return False
class VendorDataClient:

    def __init__(self):
        self.host = 'http://192.168.100.250:8080/'
        self.login = 'vendorapiuser@gmail.com'
        self.password = 'Admin321'
        self.access_token = ''
        self.csrftoken = ''
        self.refreshtoken = ''
        self.timeout = float(3)
        self.url_prefix = ''
        self.req = self._check_session()
        self.count_events = 1

    def _check_session(self):
        """Check the connection with device
         :return request.session() object
        """
        full_url = urljoin(self.host, self.url_prefix + 'vendor/api/login')
        session = requests.session()
        payload = {'username':self.login,'password':self.password}
        response = session.request(method='POST',url=full_url, data=payload)
        if response.status_code == 200:
            response_data = json.loads(response.text)
            self.access_token = "token "+response_data['api_token']
            cookies_data = response.cookies.get_dict()
            self.csrftoken = cookies_data['csrftoken']
            self.refreshtoken = cookies_data['refreshtoken']
        response.raise_for_status()
        return session

    def send_vendor_data(self):
        headers = {'Authorization': self.access_token,'X-CSRFToken':self.csrftoken}
        today = datetime.today().date()
        vendor_data_qs = VendorCompany.objects.filter(Q(created_on__date=today) | Q(update_on__date=today))
        if vendor_data_qs is not None:
            for vd in vendor_data_qs:
                payload = VendorCompanySerializer(vd).data
                response = self.req.request(
                    method='post', url=urljoin(self.host, self.url_prefix + 'vendor/api/vendor_data/'), timeout=self.timeout, stream=True, headers=headers,data=payload)
            return response.json()
        return response("No Data To Post")

   