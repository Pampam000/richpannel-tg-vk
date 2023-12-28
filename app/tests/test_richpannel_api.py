# Create an instance of the Ticket model
import json

from app.richpanel_api.request_models import Ticket, Comment, Via, Source, \
    From, To, TicketRequest
import aiohttp
import asyncio

from app.richpanel_api.response_models import TicketResponse

ticket_data = TicketRequest(ticket=Ticket(
    status="OPEN",
    comment=Comment(id="s1", body="ss1", sender_type="operator"),
    via=Via(
        channel="email",
        source=Source(
            from_=From(address="w1",
                       name="ww1"),
            to=To(address="ee1",
                  name="eee1")
        )
    ),
    tags=["eereteg"]
)
)  # response = requests.post(url, data=ticket_data.model_dump_json(), headers=headers)
ticket_data = ticket_data.model_dump()
ticket_data['ticket']['via']['source']['from'] = \
ticket_data['ticket']['via']['source']['from_']
ticket_data['ticket']['via']['source'].pop('from_')

url = "https://api.richpanel.com/v1/tickets"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-richpanel-key": "CIsPHi59Fa6Mgrk6"
}


async def main():
    async with aiohttp.ClientSession() as session:

        async with session.request(
                "POST",
                url,
                json=ticket_data,
                headers=headers,
        ) as response:

            # response = requests.post(url, data=ticket_data.model_dump_json(), headers=headers)

            # Check the response status
            if response.status == 200:
                print("Request successful")
                json_response = await response.json()
                print("Response:", json.dumps(json_response, indent=4))
                print('*'*50)
                json_response['ticket']['via']['source']['from_'] = json_response['ticket']['via']['source']['from']
                json_response['ticket']['via']['source'].pop('from')
                print(TicketResponse(**json_response))
                #print(TicketResponse(**await response.json()))
            else:
                print(f"Request failed with status code {response.status}")
                print("Response:", await response.text())


asyncio.run(main())
