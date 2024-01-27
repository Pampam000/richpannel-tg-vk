from aiohttp.web import RouteTableDef
from aiohttp.web_request import Request

from app import db
from app.create_instances import richpannel_api
from app.logger import logger
from app.tg_bot import utils as tg_utils
from app.vk import utils as vk_utils, comments_utils

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

    # comment_id: str = request['comments'][-1]['id']
    ticket: dict = await richpannel_api.conversation.retrieve_ticket(
        ticket_id=request['id'])
    logger.debug(f'ticket = {ticket}')
    messages = []
    ticket_comments = ticket['ticket']['comments']

    for comment in ticket_comments[::-1]:
        if comment['is_operator']:
            if comment['body'].startswith(
                    '{"actionName":"HTTP_TARGET_TRIGGERED_TO_COVERSATION"'):
                continue
            if await db.get_operator_answer_by_id(answer_id=comment['id']):
                continue

            messages.append({
                'message': comment['body'],
                'attachments': comment['attachments'],
                'id': comment['id'],
            })
        else:
            break

    if not messages:
        return

    customer: tuple = await db.get_customer_by_ticket_id(
        ticket_id=request['id']
    )
    logger.debug(f'customer = {customer}')
    messengers = {'vk': 1, 'tg': 2, 'vkwall':3}
    first_customer = True
    if not customer:
        first_customer = False
        ticket_customer = ticket['ticket']['via']['source']['from']['address']
        logger.debug(f'ticket_customer = {ticket_customer}')
        ticket_customer = ticket_customer.split('__')
        logger.debug(f'ticket_customer = {ticket_customer}')
        messenger_id = messengers.get(ticket_customer[1], None)
        logger.debug(f'messenger_id = {messenger_id}')
        ticket_customer = ticket_customer[0]
        logger.debug(f'ticket_customer = {ticket_customer}')
        if not messenger_id:
            return
        customer = await db.check_customer_in_db(
            email=ticket_customer,
            messenger_id=messenger_id
        )
        logger.debug(f'customer = {customer}')
        if not customer and messenger_id < 3:
            return
    for message in messages[::-1]:

        sending_kwargs = {
            "operator_message": message['message'],
            "attachments": message['attachments'],
            "user_id": customer[0],
        }

        logger.debug(f'sending_kwargs = {sending_kwargs}')
        if customer[1] == 1:
            await vk_utils.send_operator_message(**sending_kwargs)
        elif customer[1] == 2:
            await tg_utils.send_operator_message(**sending_kwargs)
        elif customer[1] == 3:
            sending_kwargs['first_comment'] = ticket_comments[0]['body'].split('\n\n')[0]
            await comments_utils.send_operator_message(**sending_kwargs)

        await db.insert_operator_answer(answer_id=message['id'])
