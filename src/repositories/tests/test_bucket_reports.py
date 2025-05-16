import unittest
from src.repositories.bucket_reports import BucketReportsRepository
from src.utils.logger import Logger
from unittest.mock import Mock, patch
from src.adapters.bucket import Bucket
from src.utils.secrets import SecretsSingleton


class TestBucketSingleton(unittest.TestCase):

    @patch('boto3.session.Session')
    def setUp(self, mock_session):
        mock_session = Mock()
        mock_client = Mock()
        mock_session.return_value.client.return_value = mock_client
        mock_client.get_secret_value.return_value = {
            'SecretString': '{"BUCKET_NAME": "test-bucket"}'
        }
        secrets = SecretsSingleton()
        self.logger = Logger()
        self.bucket = BucketReportsRepository(self.logger)
        self.mock_client = Bucket(
            secrets.get_secret('BUCKET_NAME')
        )
        self.bucket._bucket = self.mock_client
        self.mock_client.list_files.return_value = []
        self.mock_client.download_multiple_keys.return_value = []

    def test_get_all_reports(self):
        self.bucket.get_all_reports()
        self.mock_client.list_files.assert_called_once_with(
            "reports"
        )
        self.mock_client.download_multiple_keys.assert_called_once_with([])
