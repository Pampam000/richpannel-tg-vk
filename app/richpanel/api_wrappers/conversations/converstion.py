from .models import TicketRequest, UpdateTicket, \
    RetrieveByField, Ticket, From, To, Comment, Via, Source
from .models.enums import TicketStatusType, CommentSenderType, \
    TicketSubjectType, ViaChannelType
from ..base.base_wrapper import BaseRichpannelWrapper


class Conversation(BaseRichpannelWrapper):
    url = "tickets"

    async def create_ticket(
            self,
            messenger: str,
            message: str,
            channel_type: str = ViaChannelType.messenger,
            **kwargs,
    ) -> dict:
        return await self._create_ticket(
            ticket=TicketRequest(
                ticket=Ticket(
                    status=TicketStatusType.OPEN,
                    subject=getattr(TicketSubjectType, messenger),
                    comment=Comment(
                        body=message,
                        sender_type=CommentSenderType.customer
                    ),
                    via=Via(
                        channel=channel_type,
                        source=Source(
                            from_=From(**kwargs),
                            to=To()
                        )
                    ),
                    tags=[await self.api.tag.get_tag_id_by_name(messenger)],
                )
            )
        )

    async def _create_ticket(self, ticket: TicketRequest) -> dict:
        ticket:dict = ticket.model_dump()

        ticket['ticket']['via']['source']['from'] = \
            ticket['ticket']['via']['source']['from_']
        ticket['ticket']['via']['source'].pop('from_')

        response: dict = await self._request(
            method="POST",
            url=self.url,
            json=ticket)

        # response['ticket']['via']['source']['from_'] = \
        #    response['ticket']['via']['source']['from']
        # response['ticket']['via']['source'].pop('from')
        # return TicketResponse(**response)
        return response

    async def retrieve_ticket(self, ticket_id: str):
        response: dict = await self._request(
            method="GET",
            url=self.url + f'/{ticket_id}'
        )
        return response

    async def retrieve_ticket_using_customers_email_or_phone(
            self,
            ticket: RetrieveByField
    ):
        response: dict = await self._request(
            method="GET",
            url=self.url + f'/{ticket.by}/{ticket.value}'

        )
        return response

    async def update_ticket(self,
                            ticket_id: str,
                            message: str,
                            ):
        ticket = TicketRequest(
            ticket=UpdateTicket(
                comment=Comment(
                    body=message,
                    sender_type='customer',
                ),
                via=Via(
                    channel='email',
                    source=Source(
                        from_=From(address=''),
                        to=To(address='')
                    )
                )
            )
        )
        return await self._update_ticket(ticket_id=ticket_id, ticket=ticket)

    async def _update_ticket(self, ticket_id: str, ticket: TicketRequest):
        ticket = ticket.model_dump(exclude_none=True)

        ticket['ticket']['via']['source']['from'] = \
            ticket['ticket']['via']['source']['from_']
        ticket['ticket']['via']['source'].pop('from_')

        response: dict = await self._request(
            method="PUT",
            url=self.url + f'/{ticket_id}',
            json=ticket
        )
        return response
