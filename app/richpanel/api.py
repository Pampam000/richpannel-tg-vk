import aiohttp
import asyncio_atexit

from app import AsyncClass
from app.config import RICHPANNEL_TOKEN, RICHPANNEL_BASE_URL
from .api_wrappers import Conversation, Customer, Tag


class Api(AsyncClass):
    async def __init__(self):
        await super().__init__()
        await self.__prepare_session()

        self.conversation = Conversation(self.session)
        self.customer = Customer(self.session)
        self.tag = Tag(self.session)

    async def __prepare_session(self) -> None:
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-richpanel-key": RICHPANNEL_TOKEN
        }
        self.session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=10),
            base_url=RICHPANNEL_BASE_URL)
        self.session.headers.update(headers)
        asyncio_atexit.register(self.close_session)

    async def close_session(self) -> None:
        if hasattr(self, "session") and isinstance(self.session,
                                                   aiohttp.ClientSession):
            await self.session.close()
