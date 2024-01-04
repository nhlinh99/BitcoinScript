from datetime import datetime
import pytz
import logging


class BaseService():

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"SERVICE {self.__class__.__name__} IS INITIALIZED")

    def get_timezone(self):
        timezone_res = datetime.now(pytz.timezone('Asia/Saigon')).isoformat().replace("+00:00", "Z")
        return timezone_res