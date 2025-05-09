import unittest
import os
from unittest.mock import patch, MagicMock
from ..secrets import SecretsSingleton


class TestSecretsSingleton(unittest.TestCase):

    def setUp(self):
        """Set up test environment variables"""
        os.environ['SECRETS_NAME'] = 'test-secrets'
        os.environ['SECRETS_REGION'] = 'us-east-1'
        # Reset singleton instance between tests
        if hasattr(SecretsSingleton, 'instance'):
            delattr(SecretsSingleton, 'instance')

    def tearDown(self):
        """Clean up environment variables"""
        os.environ.pop('SECRETS_NAME', None)
        os.environ.pop('SECRETS_REGION', None)
        if hasattr(SecretsSingleton, 'instance'):
            delattr(SecretsSingleton, 'instance')

    def test_secrets_singleton_pattern(self):
        """Test that SecretsSingleton maintains single instance"""
        with patch('boto3.session.Session') as mock_session:
            # Configure mock to return valid JSON
            mock_client = MagicMock()
            mock_session.return_value.client.return_value = mock_client
            mock_client.get_secret_value.return_value = {
                'SecretString': '{"dummy": "value"}'
            }
            
            instance1 = SecretsSingleton()
            instance2 = SecretsSingleton()
            self.assertIs(instance1, instance2)

    @patch('boto3.session.Session')
    def test_load_secrets(self, mock_session):
        """Test loading secrets from AWS"""
        # Configure mock
        mock_client = MagicMock()
        mock_session.return_value.client.return_value = mock_client
        mock_client.get_secret_value.return_value = {
            'SecretString': '{"test_key": "test_value"}'
        }

        # Test
        secrets = SecretsSingleton()
        self.assertEqual(secrets.get_secret('test_key'), 'test_value')
        mock_client.get_secret_value.assert_called_once_with(
            SecretId='test-secrets'
        )

    @patch('boto3.session.Session')
    def test_get_secret(self, mock_session):
        """Test getting individual secrets"""
        # Configure mock
        mock_client = MagicMock()
        mock_session.return_value.client.return_value = mock_client
        mock_client.get_secret_value.return_value = {
            'SecretString': '{"test_key": "test_value"}'
        }

        # Test
        secrets = SecretsSingleton()
        self.assertEqual(secrets.get_secret('test_key'), 'test_value')
        self.assertIsNone(secrets.get_secret('non_existent'))

    @patch('boto3.session.Session')
    def test_update_secrets(self, mock_session):
        """Test updating secrets"""
        # Configure mock
        mock_client = MagicMock()
        mock_session.return_value.client.return_value = mock_client
        mock_client.get_secret_value.return_value = {
            'SecretString': '{"test_key": "test_value"}'
        }

        # Test
        secrets = SecretsSingleton()
        new_secrets = {'new_key': 'new_value'}
        secrets.update_secrets(new_secrets)

        # Verify AWS client was called correctly
        mock_client.put_secret_value.assert_called_once()
        call_kwargs = mock_client.put_secret_value.call_args[1]
        self.assertEqual(call_kwargs['SecretId'], 'test-secrets')

        # Verify local secrets were updated
        self.assertEqual(secrets.get_secret('new_key'), 'new_value')
        self.assertEqual(secrets.get_secret('test_key'), 'test_value')

    @patch('boto3.session.Session')
    def test_get_secrets(self, mock_session):
        """Test getting all secrets"""
        # Configure mock
        mock_client = MagicMock()
        mock_session.return_value.client.return_value = mock_client
        mock_client.get_secret_value.return_value = {
            'SecretString': '{"test_key": "test_value"}'
        }

        # Test
        secrets = SecretsSingleton()
        all_secrets = secrets.get_secrets()
        self.assertIsInstance(all_secrets, dict)
        self.assertEqual(all_secrets['test_key'], 'test_value')

    @patch('boto3.session.Session')
    def test_update_secrets_without_load(self, mock_session):
        """Test updating secrets without loading first"""
        # Configure mock but don't load secrets
        mock_client = MagicMock()
        mock_session.return_value.client.return_value = mock_client
        mock_client.get_secret_value.return_value = {
            'SecretString': '{"dummy": "value"}'
        }
        
        if hasattr(SecretsSingleton, 'instance'):
            delattr(SecretsSingleton, 'instance')

        # Create instance but force secrets to None
        secrets = SecretsSingleton()
        secrets._SecretsSingleton__secrets = None

        with self.assertRaises(Exception) as context:
            secrets.update_secrets({'new_key': 'new_value'})

        self.assertEqual(str(context.exception), "Secrets not loaded")
