import aiohttp


class BaseWrapper:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def _request(self,
                       method: str,
                       url: str | None = None,
                       json: dict | None = None,
                       ) -> dict:

        response: aiohttp.ClientResponse = await self.session.request(
            method=method,
            url='/v1/' + url,
            json=json
        )
        return await response.json()
