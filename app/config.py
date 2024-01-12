import os

from dotenv import load_dotenv

load_dotenv()

# common
APP_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(APP_DIR)

# richpannel
RICHPANNEL_TOKEN = os.getenv("RICHPANNEL_TOKEN")
RICHPANNEL_BASE_URL = "https://api.richpanel.com/v1/"
POLLING_TIMEOUT_BETWEEN_REQUESTS_IN_SECONDS = 10

# bot
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_START_MSG = "Здравствуйте! Здесь общается не бот, а живые люди, " \
                "поэтому ответ может занять какое-то время, спасибо за " \
                "понимание"
ADMIN_ID = 395573040

# vk
VK_GROUP_TOKEN = os.getenv('VK_GROUP_TOKEN')
VK_USER_TOKEN = os.getenv('VK_USER_TOKEN')
VK_BASE_URL = "https://api.vk.ru/method/"
VK_API_VERSION = "5.199"

# Db
DB_NAME = 'db.sqlite3'
DB_PATH = os.path.join(ROOT_DIR, DB_NAME)

# debug
DEBUG = True

# file extensions
DOCUMENT_EXTENSIONS = ['doc', 'docx', 'pdf', 'txt', 'rtf', 'odt',
                       'ppt', 'pptx', 'xls', 'xlsx', 'csv', 'html',
                       'xml', 'json', 'md', 'tex', 'zip']

PHOTO_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp',
                    'svg', 'raw', 'ico', 'heif']

VIDEO_EXTENSIONS = ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm',
                    'm4v', 'mpeg', 'mpg', '3gp', 'rm', 'swf', 'vob',
                    'ogg']
