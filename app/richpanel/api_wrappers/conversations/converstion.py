from .models import TicketRequest, UpdateTicket, \
    Ticket, From, To, Comment, Via, Source
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
        ticket_dict: dict = ticket.model_dump()

        ticket_dict['ticket']['via']['source']['from'] = \
            ticket_dict['ticket']['via']['source']['from_']
        ticket_dict['ticket']['via']['source'].pop('from_')

        response: dict = await self._request(
            method="POST",
            url=self.url,
            json=ticket_dict,
        )

        # response['ticket']['via']['source']['from_'] = \
        #    response['ticket']['via']['source']['from']
        # response['ticket']['via']['source'].pop('from')
        # return TicketResponse(**response)
        if response:
            return response
        else:
            return self._create_ticket(ticket=ticket)

    async def retrieve_ticket(self, ticket_id: str):
        response: dict = await self._request(
            method="GET",
            url=self.url + f'/{ticket_id}'
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
        ticket_dict = ticket.model_dump(exclude_none=True)

        ticket_dict['ticket']['via']['source']['from'] = \
            ticket_dict['ticket']['via']['source']['from_']
        ticket_dict['ticket']['via']['source'].pop('from_')

        response: dict | None = await self._request(
            method="PUT",
            url=self.url + f'/{ticket_id}',
            json=ticket_dict
        )
        if response:
            return response
        else:
            return await self.retrieve_ticket(ticket_id=ticket_id)
