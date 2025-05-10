from src.controllers.books import BooksController
from src.repositories.books import HarryPotterRepository
from src.utils.aws_lambda import lambda_handler


@lambda_handler
def get_all_books(event, context, logger):
    repository = HarryPotterRepository(logger)
    controller = BooksController(repository, logger)
    response = controller.get_books()
    return {
        'statusCode': 200,
        'body': [book.model_dump() for book in response]
    }


