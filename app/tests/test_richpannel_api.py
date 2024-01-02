import asyncio

from app.richpanel.api import Api
from app.richpanel.api_wrappers.conversation.models.enums import \
    TicketSubjectType, TicketStatusType, CommentSenderType
from app.richpanel.api_wrappers.conversation.models.request import Ticket, \
    Comment, Via, Source, \
    From, To, TicketRequest
from app.richpanel.api_wrappers.customer.models.request import CustomerRequest, \
    Customer


def create_ticket_request(
        subject: str,
        message: str,
        tags: list[str]
) -> TicketRequest:
    return TicketRequest(
        ticket=Ticket(
            status=TicketStatusType.OPEN,
            subject=subject,
            comment=Comment(
                body=message,
                sender_type=CommentSenderType.customer
            ),
            via=Via(
                channel='messenger',
                source=Source(
                    from_=From(id="896e9797-5a7c-4ef6-af52-dfb412ea7a5f"

                               ),
                    to=To()
                )
            ),
            tags=tags,
        )
    )


def create_customer_request():
    pass


async def main():
    api = await Api()

    vk_tag_id = await api.tag.get_tag_id_by_name('vkontakte')
    print(vk_tag_id)

    # new_customer = await api.customer.create_customer(
    #    CustomerRequest(
    #        customer=Customer(
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
        message="hello again1"
    )
    print(request_ticket.model_dump())
    #conversation = await api.conversation.create_ticket(ticket=request_ticket)


asyncio.run(main())
