import logging
from sed.logger import settings
from logging.handlers import TimedRotatingFileHandler
import sys

formatter = logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s')

stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(formatter)


file_handler = TimedRotatingFileHandler(settings.log_name,
                                        when='midnight',
                                        interval=1)
file_handler.suffix = '%Y%m%d'

