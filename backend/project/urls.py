from django.urls import path,include
from .api.login import urls as api_login_urls

urlpatterns = [
    path('api/', include(api_login_urls)),
]