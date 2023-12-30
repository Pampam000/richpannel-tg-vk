"""from aiohttp import web

async def hello(request):
    return web.Response(text="Hello, world")


app = web.Application()
# app.add_routes([web.get('/', hello)])


# https://richpanel.stickerstudio.ru/richpanel_webhook
web.run_app(app, port=8080)"""

from app.richpanel_api.api import Api
import asyncio
async def main():

    a = await Api()
    print(a)
asyncio.run(main())