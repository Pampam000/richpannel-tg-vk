import asyncio

from app.richpanel.api import Api
from app.richpanel.api_wrappers.conversations.models.enums import \
    TicketSubjectType, TicketStatusType, CommentSenderType
from app.richpanel.api_wrappers.conversations.models.request import Ticket, \
    Comment, Via, Source, \
    From, To, TicketRequest
from app.richpanel.api_wrappers.customers.models.request import CustomerRequest, \
    Customer





def create_customer_request():
    pass


async def main():
    api = await Api()

    vk_tag_id = await api.tag.get_tag_id_by_name('vkontakte')
    print(vk_tag_id)

    # new_customer = await api.customers.create_customer(
    #    CustomerRequest(
    #        customers=Customer(
    #            name='bob',
    #            phone='+79964102733'
    #        )
    #    )
    # )

    # {'identity':680825446,
    # 'labels': ['Person', 'stickerstudio176'],
    #  'properties': {
    #  'name': 'bob',
    #   'tenantId': 'stickerstudio176',
    #    'firstName': 'bob',
    #     'id': '896e9797-5a7c-4ef6-af52-dfb412ea7a5f',
    # 'phone': '+79964102733'}}
    request_ticket = create_ticket_request(
        subject=TicketSubjectType.vk.value,
        tags=[vk_tag_id],
        message="hello again11"
    )
    print(request_ticket.model_dump())
    conversation = await api.conversation.create_ticket(ticket=request_ticket)


asyncio.run(main())
