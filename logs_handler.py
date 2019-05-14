import logging
from os import environ

from telegram.ext import Updater
from telegram.error import NetworkError


class LogsHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        telegram_token = environ['TELEGRAM_TOKEN']
        self.updater = Updater(token=telegram_token)

    def emit(self, record):
        log_entry = self.format(record)
        user_id = environ['USER_ID']
        try:
            self.updater.bot.send_message(
                chat_id=user_id,
                text=log_entry
            )
        except NetworkError:
            return None


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(LogsHandler())
    return logger