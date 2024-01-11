import asyncio

from aiohttp.web import _run_app, Application

from app.tg_bot.middlewares import AlbumMiddleware, DocumentMiddleware
from app.vk import Api


async def main():
    from app.create_instances import dp, bot, create_apis
    await create_apis()
    from app.db import db_on_start
    from app.tg_bot.handlers import router
    from app.vk.handlers import router as vk_router
    from app.richpanel.handlers import router as richpanel_router

    await db_on_start()

    webhook_server = Application()
    webhook_server.add_routes(vk_router)
    webhook_server.add_routes(richpanel_router)
    #document_router.message.middleware(DocumentMiddleware())
    #photo_router.message.middleware(AlbumMiddleware())
    #dp.message.middleware(AlbumMiddleware())
    # dp.message.middleware(DocumentMiddleware())
    dp.include_router(router)
    #dp.include_router(photo_router)
    #dp.include_router(document_router)

    await bot.delete_webhook(drop_pending_updates=True)

    await asyncio.gather(
        dp.start_polling(bot),
        _run_app(webhook_server, port=8080))


asyncio.run(main())
