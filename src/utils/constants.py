import os
from src.utils.secrets import SecretsSingleton


class Constants:
    def __init__(self):
        self.__constants = None
        self.load_constants()

    def load_constants(self):
        if self.__constants is None:
            secrets = SecretsSingleton()
            self.__constants = {
                'STAGE': os.getenv('STAGE', 'dev'),
                **secrets.get_secrets()
            }
        return self.__constants

    def get(self, key):
        return self.__constants.get(key, None)
