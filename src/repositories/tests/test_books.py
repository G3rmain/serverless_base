import unittest
from unittest.mock import Mock, patch
from src.repositories.books import BooksRepository
from src.models.book import Book


class TestBooksRepository(unittest.TestCase):
    def setUp(self):
        self.mock_logger = Mock()
        self.mock_response = Mock()
        self.sample_api_response = [{
            "number": 1,
            "title": "Test Book",
            "originalTitle": "Original Test Book",
            "releaseDate": "2024-01-01",
            "description": "Test description",
            "pages": 100,
            "cover": "https://test.cover",
            "index": 0
        }]

    @patch('src.repositories.books.HarryPotterAdapterSingleton')
    def test_get_all_success(self, mock_adapter_class):
        mock_adapter = Mock()
        mock_adapter_class.return_value = mock_adapter

        self.mock_response.json.return_value = self.sample_api_response
        mock_adapter.get.return_value = self.mock_response

        repository = BooksRepository(self.mock_logger)
        books = repository.get_all()

        self.assertEqual(len(books), 1)
        self.assertIsInstance(books[0], Book)
        self.assertEqual(books[0].title, "Test Book")
        mock_adapter.get.assert_called_once_with('/en/books')

    @patch('src.repositories.books.HarryPotterAdapterSingleton')
    def test_singleton_pattern(self, mock_adapter_class):
        repo1 = BooksRepository(self.mock_logger)
        repo2 = BooksRepository(self.mock_logger)
        self.assertEqual(repo1, repo2)
