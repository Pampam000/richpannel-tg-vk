from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile

from app import config as cf
from app.config import DEVELOPER_ID
from app.create_instances import bot
from app.tg_bot.connector import TGRichpanelConnector

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(cf.BOT_START_MSG)


@router.message(Command('logs'))
async def get_logs(message: Message):
    # with open('logs/logs.log', '')
    if message.from_user.id == DEVELOPER_ID:
        file = FSInputFile('logs/logs.log')
        await bot.send_document(chat_id=DEVELOPER_ID, document=file)


@router.message(F.text | F.document | F.photo | F.video | F.sticker)
async def get_text_message(message: Message):
    await TGRichpanelConnector(message=message).process_message()
