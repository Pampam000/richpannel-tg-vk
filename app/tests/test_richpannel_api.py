import asyncio

from app.richpanel_api.api import Api
from app.richpanel_api.request_models import Ticket, Comment, Via, Source, \
    From, To, TicketRequest

ticket_data = TicketRequest(ticket=Ticket(
    status="OPEN",
    #subject='subj',
    comment=Comment(id=None, body="ss", sender_type="customer"),
    via=Via(
        channel="email",
        source=Source(
            from_=From(address="79964102733"),
                       #name="misha"),
            to=To(address="shilovmaxx.x@gmail.com",
                  name="eee1")
        )
    ),
    #tags=["eereteg"]
)
)


async def main():
    api = await Api()

    response = await api.create_ticket(ticket=ticket_data)
    print("Request successful")

    print("Response:", response)




asyncio.run(main())
