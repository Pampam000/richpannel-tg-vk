from typing import Any

from aiohttp import ClientResponse

from ..base.base_wrapper import BaseRichpannelWrapper


class Download(BaseRichpannelWrapper):

    async def file(self, url: str) -> (bytes, str):
        image_bytes: ClientResponse = await self._request(
            method="GET",
            url=url,
            use_base=False,
            headers={},
        )
        return await image_bytes.read(), self.get_file_extension(url=url)

    @staticmethod
    def get_file_extension(url: str) -> str:
        return url.split('.')[-1]

    @staticmethod
    async def _process_response(response: ClientResponse) -> dict | Any:
        return response
