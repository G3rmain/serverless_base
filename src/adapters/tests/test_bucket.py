import unittest
from src.adapters.bucket import Bucket
from unittest.mock import patch, Mock
import os
import tempfile


class TestBucketSingleton(unittest.TestCase):

    def setUp(self):

        self.bucket_name = "test-bucket"
        self.bucket = Bucket(self.bucket_name)
        self.mock_client = Mock()
        self.bucket.client = self.mock_client
        self.mock_client.upload_file.return_value = None
        self.mock_client.download_file.return_value = None

    def test_upload_file(self):
        filename = tempfile.NamedTemporaryFile().name
        with open(filename, "w") as f:
            f.write("test")
        uploaded_file = self.bucket.upload_file(filename, "test.txt")
        self.assertEqual(uploaded_file, "test.txt")
        self.mock_client.upload_file.assert_called_once_with(
            filename,
            self.bucket_name,
            "test.txt"
        )
        os.remove(filename)

    def test_download_file(self):
        filename = tempfile.NamedTemporaryFile().name
        with open(filename, "w") as f:
            f.write("test")
        self.bucket.download_file("test.txt", filename)
        self.mock_client.download_file.assert_called_once_with(
            self.bucket_name,
            "test.txt",
            filename
        )
        os.remove(filename)


