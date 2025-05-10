# decorator lambda api gateway uath
from functools import wraps
from src.utils.logger import Logger


def lambda_handler(func):
    @wraps(func)
    def wrapper(event, context):
        logger = Logger()
        logger.info(f'Event: {event}')
        logger.info(f'Context: {context}')
        try:
            function_response = func(event, context, logger)
            # logger.info(f'Function Response: {function_response}')
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
            logger.error(f'Function Error: {str(e)}')
            return {
                'statusCode': 500,
                'body': str(e)
            }
    return wrapper
