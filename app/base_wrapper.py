import asyncio
from typing import Any

from aiohttp import ClientResponse

from app import AsyncClass


class BaseWrapper:

    def __init__(self, api: AsyncClass):
        self.api = api
        self.session = api.session
        self.base_url = None

    async def _request(
            self,
            method: str,
            url: str | None = None,
            json: dict | None = None,
            data: dict | None = None,
            params: dict | None = None,
            use_base: bool = True,
            headers: dict | None = None,
    ) -> dict | Any:
        if headers is None:
            headers = self.api.headers
        response: ClientResponse = await self.session.request(
            method=method,
            url=self._format_url(url=url, use_base=use_base),
            json=json,
            params=params,
            data=data,
            headers=headers,

        )
        if response.status == 429:
            await asyncio.sleep(5)
            return await self._request(
                method=method,
                url=url,
                json=json,
                data=data,
                params=params,
                use_base=use_base,
                headers=headers
            )
        return await self._process_response(response=response)

    @staticmethod
    async def _process_response(response: ClientResponse) -> dict | Any:
        return await response.json()

    def _format_url(self, url: str, use_base: bool) -> str:
        return self.base_url + url if self.base_url and use_base else url
