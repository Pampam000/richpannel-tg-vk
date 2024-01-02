from .models.request import TicketRequest, UpdateTicket, \
    RetrieveByField
from .models.response import TicketResponse
from ..base.base_wrapper import BaseWrapper


class Conversation(BaseWrapper):
    url = "tickets"

    async def create_ticket(self, ticket: TicketRequest) -> TicketResponse:
        ticket = ticket.model_dump()

        ticket['ticket']['via']['source']['from'] = \
            ticket['ticket']['via']['source']['from_']
        ticket['ticket']['via']['source'].pop('from_')

        response: dict = await self._request(
            method="POST",
            url=self.url,
            json=ticket)
        print(0, response)
        response['ticket']['via']['source']['from_'] = \
            response['ticket']['via']['source']['from']
        response['ticket']['via']['source'].pop('from')
        print(11, response)
        # return TicketResponse(**response)
        return response

    async def retrieve_ticket(self, ticket_id: str):
        response: dict = await self._request(
            method="GET",
            url=self.url + f'/{ticket_id}'
        )
        print(22, response)
        return response

    async def retrieve_ticket_using_customers_email_or_phone(
            self,
            ticket: RetrieveByField
    ):
        response: dict = await self._request(
            method="GET",
            url=self.url + f'/{ticket.by}/{ticket.value}'

        )
        print(33, response)
        return response

    async def update_ticket(self, ticket_id: str, ticket: UpdateTicket):
        response: dict = await self._request(
            method="PUT",
            url=self.url + f'/{ticket_id}',
            json=ticket.model_dump()
        )
        print(44, response)
        return response
