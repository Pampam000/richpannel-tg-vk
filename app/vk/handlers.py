import asyncio

from aiohttp.web import Response, RouteTableDef
from aiohttp.web_request import Request

from .comment_connector import VkCommentRichpanelConnector
from .connector import VKRichpanelConnector
from ..logger import logger

router = RouteTableDef()


@router.post('/')
async def handle_new_message(request: Request) -> Response:
    request: dict = await request.json()

    if request['type'] == 'message_new':
        asyncio.ensure_future(VKRichpanelConnector(
            request=request).process_request())

    elif request['type'] == 'wall_reply_new':
        logger.debug(f'new comment request = {request}')
        asyncio.ensure_future(
            VkCommentRichpanelConnector(
                request=request
            ).process_request()
        )
    return Response(text="ok", status=200)
