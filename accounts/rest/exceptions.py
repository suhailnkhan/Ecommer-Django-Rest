from rest_framework.response import Response
from rest_framework.views import exception_handler
from datetime import datetime


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    error_messages = list()
    if response is not None:
        data = response.data.copy()
        for key_name, message in data.items():
            if isinstance(message, list):
                for msg in message:
                    error_message = str(key_name).title().replace('_', ' ') + ': ' + str(msg)
                    error_messages.append(error_message)
            else:
                error_message = str(key_name).title().replace('_', ' ') + ': ' + str(message)
                error_messages.append(error_message)

        response_data = dict()
        response_data['error_messages'] = error_messages
        response_data['status_code'] = response.status_code
        return Response(response_data, status=response.status_code, headers=response.headers)
    return response
