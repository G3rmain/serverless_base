import unittest
from unittest.mock import Mock, patch
from src.adapters.api import HarryPotterAdapterSingleton


class TestHarryPotterAdapter(unittest.TestCase):
    @patch('src.adapters.api.Constants')
    @patch('src.adapters.api.requests.Session')
    def setUp(self, mock_session, mock_constants):
        # Reset singleton state
        HarryPotterAdapterSingleton._instance = None
        HarryPotterAdapterSingleton._connection = None
        HarryPotterAdapterSingleton._base_url = None

        self.mock_session = Mock()
        mock_session.return_value = self.mock_session

        self.mock_constants = Mock()
        self.mock_constants.get.side_effect = lambda x: {
            "API_TOKEN": "test_token",
            "API_HOST": "https://api.test.com"
        }[x]
        mock_constants.return_value = self.mock_constants

        self.adapter = HarryPotterAdapterSingleton()

    def test_singleton_pattern(self):
        adapter2 = HarryPotterAdapterSingleton()
        self.assertEqual(self.adapter, adapter2)

    def test_get_request(self):
        self.adapter.get("/test")
        self.mock_session.get.assert_called_once_with(
            'https://api.test.com/test',
            params=None
        )

    def test_post_request(self):
        test_data = {"key": "value"}
        self.adapter.post("/test", test_data)
        self.mock_session.post.assert_called_once_with(
            'https://api.test.com/test',
            json=test_data
        )

    def test_put_request(self):
        test_data = {"key": "value"}
        self.adapter.put("/test", test_data)
        self.mock_session.put.assert_called_once_with(
            'https://api.test.com/test',
            json=test_data
        )

    def test_delete_request(self):
        self.adapter.delete("/test")
        self.mock_session.delete.assert_called_once_with(
            'https://api.test.com/test'
        )
