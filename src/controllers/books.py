from src.repositories.books import HarryPotterRepository


class BooksController:

    def __init__(self, books_repository: HarryPotterRepository):
        self.__books_repository = books_repository

    def get_books(self):
        books = self.__books_repository.get_all()
        return books
