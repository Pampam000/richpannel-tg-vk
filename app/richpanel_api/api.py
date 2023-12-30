import aiohttp
import asyncio_atexit

from app import AsyncClass
from app.config import RICHPANNEL_TOKEN
from app.richpanel_api.request_models import TicketRequest
from app.richpanel_api.response_models import TicketResponse


class Api(AsyncClass):
    async def __init__(self):
        await super().__init__()
        await self.__prepare_session()

    async def __prepare_session(self) -> None:
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-richpanel-key": RICHPANNEL_TOKEN
        }
        self.session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=10))
        self.session.headers.update(headers)
        asyncio_atexit.register(self.close_session)

    async def close_session(self) -> None:
        if hasattr(self, "session") and isinstance(self.session,
                                                   aiohttp.ClientSession):
            await self.session.close()

    async def create_ticket(self, ticket: TicketRequest) -> TicketResponse:
        ticket = ticket.model_dump()
        ticket['ticket']['via']['source']['from'] = \
            ticket['ticket']['via']['source']['from_']
        ticket['ticket']['via']['source'].pop('from_')
        url = "https://api.richpanel.com/v1/tickets"
        return await self.session.request(method="POST",
                                          url=url,
                                          json=ticket)
