from django.shortcuts import render
from rest_framework.exceptions import APIException
from rest_framework import status
from django.http import HttpResponse, JsonResponse

# Create your views here.
response = {}

def handler404(request, exception):
	response['errors'] = str(exception)
	response['status'] = 400
	return JsonResponse(response, content_type='application/json', 
												status=status.HTTP_500_NOT_FOUND)

def handler500(request):
	response['errors'] = "Internal Server Error"
	response['status'] = 500
	return JsonResponse(response, content_type='application/json', 
													status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def health_check(request):
    response = "OK"
    return HttpResponse(response, content_type='application/json', 
                                                    status=status.HTTP_200_OK)
