from src.adapters.api import HarryPotterAdapterSingleton
from src.models.book import Book


class HarryPotterRepository:

    _instance = None
    _adapter = None

    def __new__(cls):
        if not cls._instance:
            cls._adapter = cls.initialize_connection()
            cls._instance = super(HarryPotterRepository, cls).__new__(cls)
        return cls._instance

    @classmethod
    def initialize_connection(cls):
        return HarryPotterAdapterSingleton()

    @classmethod
    def get_all(cls):
        response = cls._adapter.get('/en/books')
        response = response.json()
        # Formatting response
        for book in response:
            book['original_title'] = book['originalTitle']
            book['release_date'] = book['releaseDate']
            book.pop('originalTitle')
            book.pop('releaseDate')
        return [Book(**book) for book in response]
