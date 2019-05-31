from rest_framework import serializers
from django.conf import settings
import datetime
import re

class SmsSerializer(serializers.Serializer):
    receiver = serializers.CharField(allow_blank=False)
    message = serializers.CharField(max_length=160, allow_blank=False, required=False, default=None)
    async_value = serializers.BooleanField(required=False, default=True)
    template = serializers.CharField(required=False, default=None)
    template_variables = serializers.DictField(required=False, child=serializers.CharField(),default=None)
    flash = serializers.IntegerField(max_value=2, default=0)
    unicode_value = serializers.CharField(max_length=5, default='auto')


    def validate_receiver(self, value):
        pattern = '^\+[1-9]{2}[0-9]{7,12}$'
        result = re.match(pattern, value)
        if result:
            return value
        else:
            raise Exception("Please enter a valid phone number.")



class BulkSmsSerializer(serializers.Serializer):
    receivers_info = serializers.ListField(
                       child=serializers.CharField(required=True),
                       allow_empty=False
                    )
    message = serializers.CharField(max_length=160, allow_blank=False, required=False, default=None)
    async = serializers.BooleanField(required=False, default=True)
    template = serializers.CharField(required=False, default=None)
    template_variables = serializers.DictField(required=False, child=serializers.CharField(),default=None)
    flash = serializers.IntegerField(max_value=2, default=0)
    unicode_value = serializers.CharField(max_length=5, default='auto')














    


