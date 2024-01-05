from aiohttp.web import Response, RouteTableDef
from aiohttp.web_request import Request

from app import db

router = RouteTableDef()


@router.post('/close_ticket')
async def handle_new_message(request: Request) -> Response:
    request: dict = await request.json()
    await db.unset_customer_ticket_id(email=request['from'])
