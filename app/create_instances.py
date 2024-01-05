from aiogram import Bot, Dispatcher
from aiohttp.web import Application

from app.config import BOT_TOKEN
from app.richpanel.api import Api as RichpannelApi

richpannel_api: RichpannelApi = None
bot = Bot(BOT_TOKEN)
dp = Dispatcher()



async def create_api():
    global richpannel_api
    richpannel_api = await RichpannelApi()
