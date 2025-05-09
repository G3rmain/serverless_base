from src.utils.constants import Constants
import requests


class HarryPotterAdapterSingleton:
    _instance = None
    _connection = None
    _base_url = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(HarryPotterAdapterSingleton, cls).__new__(cls)
            constants = Constants()
            cls._connection = requests.Session()
            cls._connection.headers.update({
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {constants.get("API_TOKEN")}'
            })
            cls._base_url = constants.get("API_HOST")
        return cls._instance

    def get(self, path, params=None):
        return self._connection.get(
            f'{self._base_url}{path}',
            params=params
        )

    def post(self, path, data=None):
        return self._connection.post(
            f'{self._base_url}{path}',
            json=data
        )

    def put(self, path, data=None):
        return self._connection.put(
            f'{self._base_url}{path}',
            json=data
        )

    def delete(self, path):
        return self._connection.delete(
            f'{self._base_url}{path}'
        )
