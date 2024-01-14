import asyncio

from aiohttp.web import Response, RouteTableDef
from aiohttp.web_request import Request

from .connector import VKRichpanelConnector

router = RouteTableDef()


@router.post('/')
async def handle_new_message(request: Request) -> Response:
    request: dict = await request.json()

    if request['type'] == 'message_new':
        asyncio.ensure_future(VKRichpanelConnector(
            request=request).process_request())
    elif request['type'] == 'wall_post_new':
        pass
    elif request['type'] == 'wall_reply_new':
        pass

    return Response(text="ok", status=200)
