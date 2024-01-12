import asyncio

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from app import config as cf
from app.tg_bot.connector import TGRichpanelConnector

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(cf.BOT_START_MSG)


@router.message(F.text | F.document | F.photo | F.video | F.sticker)
async def get_text_message(message: Message):
    await TGRichpanelConnector(message=message).process_message()


