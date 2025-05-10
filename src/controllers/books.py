from src.repositories.books import HarryPotterRepository
from src.utils.logger import Logger


class BooksController:

    def __init__(
        self,
        books_repository: HarryPotterRepository,
        logger: Logger
    ):
        self.__books_repository = books_repository
        self.__logger = logger

    def get_books(self):
        self.__logger.info('Getting books')
        books = self.__books_repository.get_all()
        self.__logger.info(f'Books: {len(books)}')
        return books
