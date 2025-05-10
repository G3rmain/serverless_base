import unittest
from src.models.book import Book


class TestBook(unittest.TestCase):
    def setUp(self):
        self.book_data = {
            "number": 1,
            "title": "Harry Potter and the Philosopher's Stone",
            "original_title": "Harry Potter and the Sorcerer's Stone",
            "release_date": "1997-06-26",
            "description": "The first book in the series",
            "pages": 223,
            "cover": "https://cover.url",
            "index": 0
        }

    def test_create_book_success(self):
        book = Book(**self.book_data)
        self.assertEqual(book.title, self.book_data["title"])
        self.assertEqual(book.pages, self.book_data["pages"])

    def test_create_book_missing_field(self):
        invalid_data = self.book_data.copy()
        del invalid_data["title"]
        with self.assertRaises(ValueError):
            Book(**invalid_data)

    def test_model_dump(self):
        book = Book(**self.book_data)
        dumped = book.model_dump()
        self.assertEqual(dumped["title"], self.book_data["title"])
        self.assertIsInstance(dumped, dict)
