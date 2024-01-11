import asyncio

from app.create_instances import richpannel_api
from app.tg_bot.utils import \
    send_operator_message as send_operator_message_to_tg
from app.vk.utils import send_operator_message as send_operator_message_to_vk

tasks = {}


async def create_task_for_checking_second_operator_answer(
        ticket_id: str,
        sleep_time: int,
        service_name: str,
        user_id: str,

) -> None:
    task = asyncio.create_task(check_second_operator_answer(
        ticket_id=ticket_id,
        sleep_time=sleep_time,
        service_name=service_name,
        user_id=user_id
    ))
    tasks[ticket_id] = task


async def check_second_operator_answer(
        ticket_id: str,
        sleep_time: int,
        service_name: str,
        user_id: str,
) -> None:
    await asyncio.sleep(sleep_time)

    ticket_response = await richpannel_api.conversation.retrieve_ticket(
        ticket_id=ticket_id
    )
    comments = ticket_response['ticket']['comments']

    if len(comments) < 2:
        return

    if comments[-1]['is_operator'] and comments[-2]['is_operator']:
        send_kwargs = {
            'user_id': user_id,
            'operator_message': comments[-1]['body'],
            'attachments': comments[-1]['attachments']
        }
        if service_name == 'vk':
            await send_operator_message_to_vk(**send_kwargs)
        elif service_name == 'tg':
            await send_operator_message_to_tg(**send_kwargs)


def pop_task(ticket_id: str):
    tasks.pop(ticket_id, None)
