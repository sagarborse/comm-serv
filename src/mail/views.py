from django.http import JsonResponse
from mail.task import sendAsyncMail
from django.template.loader import get_template
from django.template import Context
from mail.mailer import Mailer
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser
from mail.serializer import EmailSerializer, FileSerializer
from rest_framework.exceptions import ParseError
from config.output_config import *
import logging
import copy


logger = logging.getLogger("custom_logger")

@api_view(['POST'])
def sendMail(request):
	#logger.info(request.data)
	response = copy.deepcopy(output_dict)
	try:
		if not request.data:
			logger.warning('Missing input parameters.: %s', 'connection reset', extra=request.data)
			raise ValueError("Missing input parameters.")
		unserializer = EmailSerializer(data=request.data)
		logger.info(unserializer)

		if unserializer.is_valid():
			logger.info("Send Mail")
			if unserializer.data['async'] == True:
				task = sendAsyncMail.delay(unserializer.data)
				response["data"] = task.id
				response["status"]="success"
				return Response(response, content_type='application/json', 
													status=status.HTTP_200_OK)
			else:
				mailer =  Mailer(unserializer.data)
				mailer.send()
				response["data"] = unserializer.data
				response["status"] = "success"
				return Response(response, content_type='application/json', 
													status=status.HTTP_200_OK)
		else:
			response["error"] = str(unserializer.errors)
			response["status"] = "failed"
			return Response(response, content_type='application/json',
	                                    status=status.HTTP_400_BAD_REQUEST)
	except Exception as ex:
		logger.error('Something went wrong!')
		response["error"] = str(ex)
		response["status"] = "failed"
		return Response(response, content_type='application/json',
	                                    status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
@parser_classes((MultiPartParser,))
def sendMailWithAttachment(request): 
	unserializerFile = FileSerializer(data=request.data)
	response = copy.deepcopy(output_dict)
	try:
		if not unserializerFile.is_valid():
			logger.warning('Missing input parameters.: %s', 'connection reset', extra=[])
			raise ValueError("Missing input parameters.")

		unserializer = EmailSerializer(data=unserializerFile.data['json_data'])

		if unserializer.is_valid():
			logger.info("Send Mail")
			if unserializer.data['async'] == True:
				task = sendAsyncMail.delay(unserializer.data)
				if task.id is not None:
					response["data"] = task.id
					response["status"]="success"
					sts = status.HTTP_200_OK
				else:
					response["data"] = task.id
					response["status"]="failed"
					sts = status.HTTP_422_UNPROCESSABLE_ENTITY
				return Response(response, content_type='application/json', 
													status=sts)
			else:
				mailer =  Mailer(unserializer.data)
				mailer.send()
				response["status"] = "success"
				return Response(response, content_type='application/json', 
													status=status.HTTP_200_OK)
		else:
			response["error"] = unserializer.errors
			response["status"] = "failed"
			return Response(response, content_type='application/json',
	                                    status=status.HTTP_400_BAD_REQUEST)
	except ParseError as ex:
		response["error"] = "Json request syntax error"
		response["status"] = 400
		return Response(response, content_type='application/json',
	                                    status=status.HTTP_400_BAD_REQUEST)
	except Exception as ex:
		logger.error('Something went wrong!')
		response["error"] = str(ex)
		response["status"] = "failed"
		return Response(response, content_type='application/json',
	                                    status=status.HTTP_400_BAD_REQUEST)
