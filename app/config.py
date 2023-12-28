import os

import pytz
from dotenv import load_dotenv
from pytz.tzinfo import DstTzInfo

load_dotenv()

# bot
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Db
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

# admin
ADMIN_ID = 395573040


# date/time formats
TIMEZONE: DstTzInfo = pytz.timezone('Europe/Moscow')
DATE_FORMAT = "%d-%m-%Y"
TIME_FORMAT = "%H:%M"
DATETIME_FORMAT = f"{DATE_FORMAT} {TIME_FORMAT}"

# debug
DEBUG = True

