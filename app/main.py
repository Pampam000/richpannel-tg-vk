import asyncio

from aiohttp.web import _run_app, Application

from app.tg_bot.middlewares import AlbumMiddleware, DocumentMiddleware
from app.vk import Api


async def main():
    from app.create_instances import dp, bot, create_api
    await create_api()
    from app.db import db_on_start
    from app.tg_bot.handlers import router
    from app.vk.handlers import router as vk_router
    from app.richpanel.handlers import router as richpanel_router

    await db_on_start()
    #vk_api = await Api()
    a = "https://richpanel-data.s3.us-west-2.amazonaws.com" \
        " /MessengerAttachments/45693c3d-5692-4345-a576-2c32fd753887/2.jpg"
    url1 = 'https://richpanel-data.s3.us-west-2.amazonaws.com' \
           '/MessengerAttachments/45693c3d-5692-4345-a576-2c32fd753887/2.jpg'
    # url1 = 'https://google.com'
    # print(a == url1)
    # png = "https://richpanel-data.s3.us-west-2.amazonaws.com
    # /MessengerAttachments/1159e795-5b78-46ec-b6b2-3ce97037feb2/1159e795-5b78-46ec-b6b2-3ce97037feb2.png"
    # pdf = "https://richpanel-data.s3.us-west-2.amazonaws.com
    # /MessengerAttachments/8f1b795b-86ec-452d-ae2a-725d2c54d04b/8f1b795b-86ec-452d-ae2a-725d2c54d04b.pdf"
    #
    # photo: bytes = await richpannel_api.download.photo(url=pdf)
    # attachment: dict = await vk_api.document.upload(peer_id=52100128,
    #                                            file=photo,
    #                                                file_format='pdf')
    # print(attachment)
    # response: dict = await vk_api.message.send(
    #    user_id=52100128,
    #    attachment=attachment,
    #    message='yoyoyoy'
    # )
    # print(response)
    # return
    webhook_server = Application()
    webhook_server.add_routes(vk_router)
    webhook_server.add_routes(richpanel_router)
    #document_router.message.middleware(DocumentMiddleware())
    #photo_router.message.middleware(AlbumMiddleware())
    # dp.message.middleware(CounterMiddleware())
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
