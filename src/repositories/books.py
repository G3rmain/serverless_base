from src.adapters.api import HarryPotterAdapterSingleton
from src.models.book import Book
from src.utils.logger import Logger


class HarryPotterRepository:

    _instance = None
    _adapter = None
    _logger: Logger = None

    def __new__(cls, logger):
        if not cls._instance:
            cls._adapter = cls.initialize_connection()
            cls._instance = super(HarryPotterRepository, cls).__new__(cls)
        cls._logger = logger
        return cls._instance

    @classmethod
    def initialize_connection(cls):
        return HarryPotterAdapterSingleton()

    @classmethod
    def get_all(cls):
        cls._logger.info('Getting books')
        response = cls._adapter.get('/en/books')
        response = response.json()
        # cls._logger.info(f'Books: {response}')
        # Formatting response
        for book in response:
            book['original_title'] = book['originalTitle']
            book['release_date'] = book['releaseDate']
            book.pop('originalTitle')
            book.pop('releaseDate')
        return [Book(**book) for book in response]
