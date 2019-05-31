from celery.decorators import task
from celery.utils.log import get_task_logger
from mail.mailer import Mailer
import copy

logger = get_task_logger(__name__)


@task(name="sendAsyncMail")
def sendAsyncMail(data):
    """sends an email when feedback form is filled successfully"""
    mail_data = copy.deepcopy(data)
    for recipient in data['recipients']:
    	mail_data['recipients'] = [recipient]
    	mailer =  Mailer(mail_data)
    	Mailer.send()
    
    logger.info("Sent mail with celery")
    return '{} random users created with success!'.format(mail_data)