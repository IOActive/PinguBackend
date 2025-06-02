from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError


def custom_exception_handler(exc, context):
    # Call DRF's default exception handler to get the standard error response.
    response = exception_handler(exc, context)

    # If a response was returned by the exception handler, customize it.
    if response is not None:
        custom_response = {
            'status': response.status_code,
            'message': None,
            'errors': {},
            'success': False
        }
        
        # Try to get the error message from different fields
        detail = response.data.get('detail')
        error = response.data.get('error')
        
        if detail is not None:
            custom_response['message'] = detail
            custom_response['errors'] = response.data
        elif error is not None:
            custom_response['message'] = error
            custom_response['errors'] = response.data
        else:
            # Fallback to the default DRF behavior if no specific field is found
            custom_response['message'] = 'An error occurred'
            custom_response['errors'] = response.data
        return Response(custom_response, status=response.status_code)

    # If the exception is not handled by DRF (e.g., validation errors), handle it here.
    if isinstance(exc, ValidationError):
        custom_response = {
            'status': status.HTTP_400_BAD_REQUEST,
            'message': exc.error_list[0],
            'errors': exc.error_list,
            'success': False
        }
        return Response(custom_response, status=status.HTTP_400_BAD_REQUEST)

    # If the exception is not handled by DRF and it's a generic error, handle it here.
    custom_response = {
        'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
        'message': str(exc),
        'errors': {},
        'success': False
    }
    return Response(custom_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)