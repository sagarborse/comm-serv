from rest_framework.views import exception_handler
import logging

logger = logging.getLogger("custom_logger")

def custom_exception_handler(exc, context):
	# Call REST framework's default exception handler first,
	# to get the standard error response.
	response = exception_handler(exc, context)

	if not response:
		# Unhandled exceptions (500 internal server errors)
		response = Response(data={
			'error': 'server_error',
			'error_description': unicode(exc).replace('"',"'"),
		}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

		logger.info(unicode(exc).replace('"',"'"))
		return response


	if hasattr(exc, 'default_error'):
		response.data['error_type'] = exc.default_error
	else:
		response.data['error_type'] = 'api_error'

	if 'detail' in response.data:
		response.data['error'] = response.data['detail'].replace('"',"'")
		del response.data['detail']
	elif hasattr(exc, 'default_detail'):
		response.data['error_description'] = exc.default_detail.replace('"',"'")


	response.data['status_code'] = response.status_code

	logger.log('An error occured %s', response.data['error_description']);

	return response