from django.urls import re_path
from .views import send_sms, send_bulk_sms

urlpatterns=[
    re_path(r'^send/$',send_sms, name='send_sms'),
    re_path(r'^bulk-send/$',send_bulk_sms, name='send_bulk_sms'),
]