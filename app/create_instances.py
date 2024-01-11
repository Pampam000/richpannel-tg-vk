from aiogram import Bot, Dispatcher

from app.config import BOT_TOKEN
from app.richpanel.api import Api as RichpannelApi
from app.vk import Api as VK_API

richpannel_api: RichpannelApi | None = None
vk_api: VK_API | None = None
bot = Bot(BOT_TOKEN)
dp = Dispatcher()


async def create_apis():
    global richpannel_api, vk_api
    richpannel_api = await RichpannelApi()
    vk_api = await VK_API()
