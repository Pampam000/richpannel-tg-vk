import asyncio

from app.vk.api import Api

async def main():
    api = await Api()
    response = await api.get_longpoll_server()

asyncio.run(main())