import sys
from logging import getLogger, StreamHandler, Formatter, DEBUG, INFO, \
    FileHandler
from app import config as cf

log_format = '%(asctime)s [%(levelname)s][%(pathname)s: %(funcName)s: ' \
             '%(lineno)d]: %(message)s'

stream_handler = StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(Formatter(fmt=log_format))

file_handler = FileHandler(filename='./logs/logs.log', encoding='utf-8')
file_handler.setFormatter(Formatter(fmt=log_format))

logger = getLogger(__name__)

if cf.DEBUG:
    logger.setLevel(DEBUG)
else:
    logger.setLevel(INFO)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)