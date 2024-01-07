import os

import pytz
from dotenv import load_dotenv
from pytz.tzinfo import DstTzInfo

load_dotenv()

# common
APP_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(APP_DIR)

# richpannel
RICHPANNEL_TOKEN = os.getenv("RICHPANNEL_TOKEN")
RICHPANNEL_BASE_URL = "https://api.richpanel.com/v1/"

# bot
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_START_MSG = "Здравствуйте! Здесь общается не бот, а живые люди, " \
                "поэтому ответ может занять какое-то время, спасибо за " \
                "понимание"
ADMIN_ID = 395573040

# vk
VK_GROUP_TOKEN = os.getenv('VK_GROUP_TOKEN')
VK_BASE_URL = "https://api.vk.ru/method/"
VK_API_VERSION = "5.199"

# Db
DB_NAME = 'db.sqlite3'
DB_PATH = os.path.join(ROOT_DIR, DB_NAME)

# date/time formats
TIMEZONE: DstTzInfo = pytz.timezone('Europe/Moscow')
DATE_FORMAT = "%d-%m-%Y"
TIME_FORMAT = "%H:%M"
DATETIME_FORMAT = f"{DATE_FORMAT} {TIME_FORMAT}"

# debug
DEBUG = True
