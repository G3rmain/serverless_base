from src.adapters.bucket import Bucket
from src.utils.logger import Logger
from src.utils.constants import Constants


class BucketReportsRepository:

    _instance = None
    _bucket = None
    _logger: Logger = None

    def __init__(self, logger: Logger):
        self._logger = logger
        self._bucket = Bucket(Constants.BUCKET_NAME)

    def get_all_reports(self):
        self._logger.info('Getting all reports from bucket')
        bucket_files = self._bucket.list_files('reports')
        files = self._bucket.download_multiple_keys(
            [f['Key'] for f in bucket_files]
        )
        return files
