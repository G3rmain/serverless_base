from src.controllers.books import BooksController
from src.repositories.books import BooksRepository
from src.utils.aws_lambda import lambda_handler


@lambda_handler
def get_all_books(event, context, logger):
    repository = BooksRepository(logger)
    controller = BooksController(repository, logger)
    response = controller.get_books()
    return {
        'statusCode': 200,
        'body': response
    }
