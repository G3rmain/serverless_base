# decorator lambda api gateway uath
from functools import wraps
from src.utils.logger import Logger
import uuid


def lambda_handler(func):
    @wraps(func)
    def wrapper(event, context):
        trace_id = str(uuid.uuid4())
        logger = Logger(trace_id)
        logger.info('Event: ', event)
        logger.info('Context: ', context)
        try:
            function_response = func(event, context, logger)
            logger.info('Function Response: ', function_response)
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
            logger.error('Function Error: ', str(e))
            return {
                'statusCode': 500,
                'body': str(e)
            }
    return wrapper
