import asyncio

from aiohttp.web import Response, RouteTableDef
from aiohttp.web_request import Request

from .connector import VKRichpanelConnector

router = RouteTableDef()


@router.post('/')
async def handle_new_message(request: Request) -> Response:
    asyncio.ensure_future(VKRichpanelConnector().process_request(
        request=request)
    )
    return Response(text="ok", status=200)
