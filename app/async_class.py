import aiohttp
import asyncio_atexit


class AsyncClass:
    base_url = ""
    headers = {}

    async def __new__(cls, *a, **kw):
        instance = super().__new__(cls)
        await instance.__init__(*a, **kw)
        return instance

    async def __init__(self):
        await self._prepare_session()

    async def _prepare_session(self) -> None:
        self.session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=10),
            base_url=self.base_url)
        self.session.headers.update(self.headers)
        asyncio_atexit.register(self._close_session)

    async def _close_session(self) -> None:
        if hasattr(self, "session") and isinstance(self.session,
                                                   aiohttp.ClientSession):
            await self.session.close()
