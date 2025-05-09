import boto3
import json
import os


class SecretsSingleton:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SecretsSingleton, cls).__new__(cls)
            cls.instance.__secrets = None
            cls.instance.load_secrets()
        return cls.instance

    def load_secrets(self):
        if self.__secrets is None:
            secret_name = os.environ['SECRETS_NAME']
            region_name = os.environ['SECRETS_REGION']
            print(f'Loading secrets: {secret_name} in {region_name}')
            session = boto3.session.Session()
            client = session.client(
                service_name='secretsmanager',
                region_name=region_name,
            )
            secret_string = client.get_secret_value(
                SecretId=secret_name
            )['SecretString']
            self.__secrets = json.loads(secret_string)
            print('Secrets loaded successfully')
        return self.__secrets

    def get_secret(self, key):
        return self.__secrets.get(key, None)

    def update_secrets(self, new_secrets):
        if self.__secrets is not None:
            secret_name = os.environ['SECRETS_NAME']
            region_name = os.environ['SECRETS_REGION']
            print(f'Updating secrets: {secret_name} in {region_name}')
            session = boto3.session.Session()
            client = session.client(
                service_name='secretsmanager',
                region_name=region_name,
            )
            new_secrets = {
                **self.__secrets,
                **new_secrets
            }
            client.put_secret_value(
                SecretId=secret_name,
                SecretString=json.dumps(new_secrets)
            )
            self.__secrets = {**new_secrets}
            print('Secrets updated successfully')
        else:
            raise Exception("Secrets not loaded")

    def get_secrets(self):
        return self.__secrets
