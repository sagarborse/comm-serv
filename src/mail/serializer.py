from rest_framework import serializers
from django.conf import settings
import logging
import json

logger = logging.getLogger("custom_logger")

#REQUEST SERIALIZERS
class EmailSerializer(serializers.Serializer):
    """
    Serializer for verifying if the request by the email API is valid
    """
    
    sender = serializers.EmailField(required=False, default=settings.DEFAULT_FROM_EMAIL)
    recipients = serializers.ListField(
       child=serializers.EmailField(allow_blank=False),
       allow_empty=False
    )
    cc = serializers.ListField(
       child=serializers.EmailField(),
       required=False,
       default=None
    )
    bcc = serializers.ListField(
       child=serializers.EmailField(),
       required=False,
       default=None
    )
    subject = serializers.CharField(required=False, default=None)
    template = serializers.CharField(required=False, default=None)
    message = serializers.CharField(required=False, default=None)
    headers = serializers.CharField(required=False, default=None)
    template_variables = serializers.DictField(child=serializers.CharField(),default=None)
    multipart = serializers.BooleanField(required=False, default=False)
    async = serializers.BooleanField(required=False, default=True)




class FileSerializer ( serializers.Serializer ) :

    json_file = serializers.FileField( max_length=100000, allow_empty_file=False,
                                            use_url=False, required=True )

    attachment = serializers.ListField(
                                child=serializers.FileField( max_length=100000,allow_empty_file=False,
                                         use_url=False, required=True ), 
                                allow_empty=False )

    json_data = serializers.DictField(required=False, default=None)


    def validate_json_file(self, value):
      data = ''
      for line in value:
        data = data + line.decode()

      self.json_data = data

      return value


    def validate_json_data(self, value):
      dictdump = json.loads(self.json_data)

      return dictdump











    


