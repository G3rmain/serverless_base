import unittest
from unittest.mock import Mock
from src.controllers.books import BooksController
from src.models.book import Book


class TestBooksController(unittest.TestCase):
    def setUp(self):
        self.mock_logger = Mock()
        self.mock_repository = Mock()
        self.controller = BooksController(
            books_repository=self.mock_repository,
            logger=self.mock_logger
        )
        self.sample_book = Book(
            number=1,
            title="Test Book",
            original_title="Original Test Book",
            release_date="2024-01-01",
            description="Test description",
            pages=100,
            cover="https://test.cover",
            index=0
        )

    def test_get_books_success(self):
        self.mock_repository.get_all.return_value = [self.sample_book]
        result = self.controller.get_books()

        self.mock_repository.get_all.assert_called_once()
        self.mock_logger.info.assert_called()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Test Book")

    def test_get_books_empty(self):
        self.mock_repository.get_all.return_value = []
        result = self.controller.get_books()

        self.mock_repository.get_all.assert_called_once()
        self.assertEqual(len(result), 0)
