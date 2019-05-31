from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view
from django.http import JsonResponse
from sms.serializer import SmsSerializer, BulkSmsSerializer
from config.output_config import *
from rest_framework.response import Response
from rest_framework import status
from sms.kaleyraSmsGateway import KaleyraSmsGateway
from sms.task import sendAsyncSms
import copy
import logging


logger = logging.getLogger("custom_logger")

@api_view(['POST'])
def send_sms(request):
	response = copy.deepcopy(output_dict)
	try:
		if not request.data:
			logger.warning('Missing input parameters.: %s', 'connection reset', extra=request.data)
			raise ValueError("Missing input parameters.")
		unserializer = SmsSerializer(data=request.data)

		if unserializer.is_valid():
			logger.info("Send SMS")
			if unserializer.data['async_value'] == True:
				task = sendAsyncSms.delay(unserializer.data)
				response["data"] = task.id
				response["status"]="success"
				return Response(response, status=status.HTTP_200_OK)
			else:
				sms =  KaleyraSmsGateway(unserializer.data)
				res = sms.send()
				response["data"] = res
				response["status"] = "success"
				return Response(response, status=status.HTTP_200_OK)
		else:
			response["error"] = unserializer.errors
			response["status"] = "failed"
			return Response(response, status=status.HTTP_400_BAD_REQUEST)
	except Exception as ex:
		logger.error('Something went wrong!')
		response["error"] = str(ex)
		response["status"] = "failed"
		return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def send_bulk_sms(request):
	logger.info("Sms start")
	response = copy.deepcopy(output_dict)
	try:
		if not request.data:
			logger.warning('Missing input parameters.: %s', 'connection reset', extra=request.data)
			raise ValueError("Missing input parameters.")
		unserializer = BulkSmsSerializer(data=request.data)

		if unserializer.is_valid():
			for receiver in unserializer.data['receivers_info']:
				receiver_data = request.data
				receiver_data['receiver'] = receiver
				
				unserializer = SmsSerializer(data=receiver_data)
				if unserializer.is_valid():
					logger.info("Send SMS")
					if unserializer.data['async_value'] == True:
						task = sendAsyncSms.delay(unserializer.data)
						response["data"] = task.id
						response["status"]="success"
						return Response(response, status=status.HTTP_200_OK)
					else:
						sms =  KaleyraSmsGateway(unserializer.data)
						res = sms.send()
						response["data"] = res
						response["status"] = "success"
						return Response(response, status=status.HTTP_200_OK)
				else:
					response["error"] = unserializer.errors
					response["status"] = "failed"
		else:
			response["error"] = unserializer.errors
			response["status"] = "failed"
		

		return Response(response, status=status.HTTP_400_BAD_REQUEST)
	except Exception as ex:
		logger.error('Something went wrong!')
		response["error"] = str(ex)
		response["status"] = "failed"
		return Response(response, status=status.HTTP_400_BAD_REQUEST)