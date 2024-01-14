from aiohttp.web import RouteTableDef
from aiohttp.web_request import Request

from app import db
from app.create_instances import richpannel_api
from app.logger import logger
from app.tg_bot import utils as tg_utils
from app.vk import utils as vk_utils

router = RouteTableDef()


@router.post('/close_ticket')
async def handle_close_ticket(request: Request) -> None:
    request: dict = await request.json()
    logger.debug(f'close ticket request={request}')
    await db.unset_customer_ticket_id(ticket_id=request['id'])


@router.post('/webhook')
async def handle_webhook(request: Request):
    request: dict = await request.json()
    logger.debug(f'webhook request={request}')

    if len(request['comments']) >= 2 and \
            request['comments'][-1]['authorEmail'] != request['comments'][-2][
        'authorEmail']:
        return

    comment_id: str = request['comments'][-1]['id']
    ticket: dict = await richpannel_api.conversation.retrieve_ticket(
        ticket_id=request['id'])
    logger.debug(ticket)
    message = None
    attachments = []

    for comment in ticket['ticket']['comments']:
        if comment['id'] == comment_id:
            message: str = comment['body']
            attachments: list[str] = comment['attachments']
            break

    if not (message or attachments):
        return

    customers: list[tuple] = await db.get_customers_by_ticket_id(
        ticket_id=request['id']
    )
    logger.debug(f'customers = {customers}')
    sending_kwargs = {
        "operator_message": message,
        "attachments": attachments
    }
    for customer in customers:
        sending_kwargs['user_id'] = customer[0]
        logger.debug(f'sending_kwargs = {sending_kwargs}')
        if customer[1] == 1:
            await vk_utils.send_operator_message(**sending_kwargs)
        elif customer[1] == 2:
            await tg_utils.send_operator_message(**sending_kwargs)
