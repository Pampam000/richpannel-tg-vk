import aiohttp


class BaseWrapper:

    def __init__(self, api):
        self.api = api
        self.session = api.session
        self.base_url = None

    async def _request(
            self,
            method: str,
            url: str | None = None,
            json: dict | None = None,
    ) -> dict:
        response: aiohttp.ClientResponse = await self.session.request(
            method=method,
            url=self._format_url(url=url),
            json=json
        )
        return await response.json()

    def _format_url(self, url: str):
        return self.base_url + url if self.base_url else url
