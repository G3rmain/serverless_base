# decorator lambda api gateway uath
from functools import wraps


def lambda_handler(func):
    @wraps(func)
    def wrapper(event, context):
        print('Event: ', event)
        print('Context: ', context)
        try:
            function_response = func(event, context)
            # print('Function Response: ', str(function_response))
            if (
                isinstance(function_response, dict) and
                'statusCode' in function_response and
                'body' in function_response
            ):
                return function_response
            else:
                return {
                    'statusCode': 200,
                    'body': function_response
                }
        except Exception as e:
            # print('Function Error: ', str(e))
            return {
                'statusCode': 500,
                'body': str(e)
            }
    return wrapper
