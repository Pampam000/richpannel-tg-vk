import asyncio
from typing import TYPE_CHECKING, Any

from aiohttp import ClientResponse

from app.base_wrapper import BaseWrapper
from app.logger import logger

if TYPE_CHECKING:
    from app.richpanel import Api

from app import config as cf


class BaseRichpannelWrapper(BaseWrapper):

    def __init__(self, api: "Api"):
        super().__init__(api=api)
        self.base_url: str = cf.RICHPANNEL_BASE_URL

    async def _process_response(
            self,
            response: ClientResponse,
            request_kwargs: dict | None = None
    ) -> dict | Any:
        if await self._check_429_error(response=response,
                                       request_kwargs=request_kwargs):
            return
        elif await self._check_timeout_error(
                response=response,
                request_kwargs=request_kwargs,
        ):
            return
        elif result:=await self._check_conversation_does_not_exist(
                response=response,
                request_kwargs=request_kwargs,
        ):
            return result

        return await super()._process_response(response=response)

    async def _check_429_error(self, response: ClientResponse,
                               request_kwargs: dict):
        if response.status == 429:
            logger.debug('429 ERROR was occurred')
            await asyncio.sleep(5)
            return await self._request(**request_kwargs)

    async def _check_timeout_error(self, response: ClientResponse,
                                   request_kwargs: dict):
        response: dict = await response.json()
        if 'message' in response:
            if response['message'] == 'Endpoint request timed out':
                logger.debug('GOT ENDPOINT TIME OUT')
                await asyncio.sleep(5)
                return True
                # return await self._request(**request_kwargs)

    async def _check_conversation_does_not_exist(self,
                                                 response: ClientResponse,
                                                 request_kwargs: dict):
        response: dict = await response.json()
        if 'errors' in response and 'message' in response['errors']:
            if response['errors']['message'] == ('Provided conversation id '
                                                 'does not exist.'):
                logger.debug('NO CONVESATION WITH THE GIVEN ID')
                await asyncio.sleep(10)
                return await self._request(**request_kwargs)
        elif 'error' in response and 'message' in response['error']:
            if response['error']['message'] == ('No conversations found with '
                                                'the given Id.'):
                logger.debug('NO CONVESATION WITH THE GIVEN ID')
                await asyncio.sleep(10)
                return await self._request(**request_kwargs)