import logging
import abc
import uuid


class AbstractLoggerService(abc.ABC):
    @abc.abstractmethod
    def info(self, message: str, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def debug(self, message: str, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def warning(self, message: str, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def error(self, message: str, **kwargs):
        raise NotImplementedError


class Logger(AbstractLoggerService):

    def __init__(self, trace_id: str = None):
        self.trace_id = trace_id or str(uuid.uuid4())
        self.logger = logging.getLogger(self.trace_id)
        self.logger.setLevel(logging.INFO)
        if not self.logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def info(self, message: str, **kwargs):
        self.logger.info(self._format(message, kwargs))

    def debug(self, message: str, **kwargs):
        self.logger.debug(self._format(message, kwargs))

    def warning(self, message: str, **kwargs):
        self.logger.warning(self._format(message, kwargs))

    def error(self, message: str, **kwargs):
        self.logger.error(self._format(message, kwargs))

    def exception(self, message: str, **kwargs):
        self.logger.exception(self._format(message, kwargs))

    def _format(self, message: str, data: dict):
        return f"[{self.trace_id}] {message}"
