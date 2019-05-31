from celery.decorators import task
from celery.utils.log import get_task_logger
from sms.kaleyraSmsGateway import KaleyraSmsGateway
import copy
import logging

logger = get_task_logger(__name__)


@task(name="sendAsyncSms")

def sendAsyncSms(sms_data):
	"""sends an email when feedback form is filled successfully"""
	sms =  KaleyraSmsGateway(sms_data)
	sms.send()

	logger.info("Sent sms with celery {}".format(str(sms_data)))
	return '{} random users created with success!'.format(str(sms_data))



