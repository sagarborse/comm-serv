from django.template import Context
from django.conf import settings
from django.template.loader import get_template
from render_block import render_block_to_string
import requests
import logging

logger = logging.getLogger("custom_logger")


class KaleyraSmsGateway(object): 

	@classmethod
	def __init__(self, data):
		self.smsInfo = data
		self.serviceProvider = "https://{0}/v4/?".format(settings.SMS_HOST)

	@classmethod
	def send(self):
		if self.smsInfo['template']:
			if self.smsInfo['message']:
				logger.info("You can\'t specify both \'template\' and \'message\' arguments")
				raise ValueError('You can\'t specify both \'template\' and \'message\' arguments')

		context = self.smsInfo['template_variables']

		if self.smsInfo['template'] is not None:
			template_name = "sms_templates/{0}.html".format(self.smsInfo['template'])
			text_message = render_block_to_string(template_name, 'plain', context)
		else :
			if not self.smsInfo['message']:
				logger.info("'message' argument is missing")
				raise ValueError('\'message\' argument is missing')
			text_message = self.smsInfo['message']
		

		queryString = {}
		queryString['to'] = self.smsInfo['receiver']
		queryString['sender'] = settings.SMS_SENDER
		queryString['api_key'] = settings.SMS_API_KEY
		queryString['message'] = text_message
		queryString['method'] = settings.KALERYA_METHOD

		response = requests.get(self.serviceProvider, params=queryString, timeout=(3,5))
		response.raise_for_status()

		
		return response


