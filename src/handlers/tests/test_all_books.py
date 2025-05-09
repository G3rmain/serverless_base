import unittest
from src.handlers.all_books import get_all_books
from src.utils.secrets import SecretsSingleton
from unittest.mock import patch
from unittest.mock import MagicMock
from unittest.mock import Mock


def mock_load_secrets(self):
    print('Mocking load secrets')
    self.__secrets = {
        'API_HOST': 'https://api.example.com',
        'API_TOKEN': 'token'
    }


class TestAllBooks(unittest.TestCase):

    def setUp(self):
        # Mock secrets
        SecretsSingleton.load_secrets = Mock()
        SecretsSingleton.load_secrets.side_effect = mock_load_secrets

    def test_success(self):
        response = get_all_books(None, None)
        self.assertEqual(response['statusCode'], 200)
        self.assertIsInstance(response['body'], list)

    def test_failure(self):
        with patch(
            'src.repositories.books.HarryPotterRepository.get_all',
            side_effect=Exception('Error')
        ):
            response = get_all_books(None, None)
            self.assertEqual(response['statusCode'], 500)
            self.assertEqual(response['body'], 'Error')
