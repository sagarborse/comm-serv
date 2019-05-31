from django.template import Context
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from .utils import (parse_emails)
from render_block import render_block_to_string


class Mailer(object): 

	@classmethod
	def __init__(self, data):
		self.mailInfo = data

	@classmethod
	def send(self):
		if self.mailInfo['template']:
			if self.mailInfo['message']:
				raise ValueError('You can\'t specify both \'template\' and \'message\' arguments')

		context = self.mailInfo['template_variables']

		if self.mailInfo['template'] is not None:
			template_name = "email_templates/{0}.html".format(self.mailInfo['template'])
			subject_alternative = render_block_to_string(template_name, 'subject', context)
			text_alternative = render_block_to_string(template_name, 'plain', context)
			html_alternative = render_block_to_string(template_name, 'html', context)

			msg = EmailMultiAlternatives(self.mailInfo['subject'], text_alternative,
					self.mailInfo['sender'], self.mailInfo['recipients'], bcc=self.mailInfo['bcc'], 
					cc=self.mailInfo['cc'], headers=self.mailInfo['headers'])
			msg.attach_alternative(html_alternative, "text/html")

			return msg.send(fail_silently=False)
		else :
			if not self.mailInfo['subject'] or not self.mailInfo['message']:
				raise ValueError('\'subject\'  or \'message\' argument is missing')
			msg = EmailMessage(
                subject=self.mailInfo['subject'], body=self.mailInfo['message'], from_email=self.mailInfo['sender'],
                to=self.mailInfo['recipients'], bcc=self.mailInfo['bcc'], cc=self.mailInfo['cc'],
                headers=self.mailInfo['headers'])
			msg.content_subtype = "html"
			
			return msg.send(fail_silently=False)


