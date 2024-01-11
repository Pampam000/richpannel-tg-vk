from aiohttp.web import Response, RouteTableDef
from aiohttp.web_request import Request

from app import db
from app.logger import logger

router = RouteTableDef()


@router.post('/close_ticket')
async def handle_new_message(request: Request) -> Response:
    request: dict = await request.json()
    logger.debug(f'close ticket request={request}')
    await db.unset_customer_ticket_id(email=request['from'])
