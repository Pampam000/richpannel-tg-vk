import asyncio

from aiohttp.web_request import Request
from bs4 import BeautifulSoup

from app.create_instances import richpannel_api
from .api import Api
from .api_wrappers.users.models.response import UserModel
from .. import db


class VKRichpanelConnector:
    def __init__(self):
        self.request = None
        self.vk_api = None
        self.message = None
        self.user_id = None
        self.attachments = None
        self.text = None
        self.ticket_id = None
        self.processed_attachments = []

    async def process_request(self, request: Request):
        self.request: dict = await request.json()
        self.message: dict = self.request['object']['message']
        self.attachments: list = self.message['attachments']
        self.process_attachments()
        self.text: str = self.message['text']
        user_id = self.message['from_id']
        self.vk_api = await Api()
        user: UserModel = await self.vk_api.user.get_user_by_id(user_id)
        self.user_id = str(user.id) * 2 + "12"

        customer_response = await richpannel_api.customer.create_customer(
            email=self.user_id,
            name=user.first_name + " " + user.last_name,
        )

        if 'error' in customer_response:
            print('ERRROR')
            self.ticket_id = await db.get_customer_ticket_id(
                email=self.user_id)
            print(self.ticket_id)

            if self.ticket_id:
                await self._send_vk_message_if_ticket_is_open()
            else:
                await self._send_vk_message_if_ticket_is_closed()
            return
        await self._send_vk_message_if_no_ticket()

    async def _send_vk_message_if_ticket_is_closed(self):
        message_response, self.ticket_id = await \
            self._get_message_response_and_ticket_id()
        print(333, message_response)
        await db.update_customer_ticket_id(
            email=self.user_id,
            ticket_id=self.ticket_id
        )
        await self._send_vk_message(response=message_response)

    async def _send_vk_message_if_no_ticket(self):
        message_response, self.ticket_id = await \
            self._get_message_response_and_ticket_id()
        print(222, message_response)
        await db.create_customer(
            email=self.user_id,
            messenger_id=1,
            ticket_id=self.ticket_id
        )

        await self._send_vk_message(response=message_response)

    async def _send_vk_message_if_ticket_is_open(self):
        update_response = await richpannel_api.conversation.update_ticket(
            ticket_id=self.ticket_id,
            message=self._create_richpannel_message()
        )
        print(444, update_response)
        await self._send_vk_message(response=update_response)

    async def _get_message_response_and_ticket_id(self) -> tuple:
        message_response = await richpannel_api.conversation.create_ticket(
            messenger='vkontakte',
            message=self._create_richpannel_message(),
            channel_type='email',
            address=self.user_id,
        )
        print(message_response)
        print()
        ticket_id: str = message_response['ticket']['id']
        print(ticket_id)
        return message_response, ticket_id

    async def _send_vk_message(self, response: dict):
        comments_amount = len(response['ticket']['comments'])
        print(comments_amount)

        operator_message: str | None = await self._check_operator_answer(
            comments_amount=comments_amount,
            ticket_id=self.ticket_id
        )

        print(operator_message)
        print('#' * 20)

        vk_message = await self.vk_api.message.send_message(
            user_id=52100128,
            message=operator_message
        )
        print(vk_message)

    async def _check_operator_answer(
            self,
            comments_amount: int,
            ticket_id: str
    ) -> dict | None:
        a = comments_amount
        comments = []
        while 1:
            response = await richpannel_api.conversation.retrieve_ticket(
                ticket_id=ticket_id
            )
            print('*' * 20)
            print(response)
            print('*' * 20)
            if 'error' in response:
                await asyncio.sleep(10)
                continue
            comments = response['ticket']['comments']
            comments_amount = len(comments)
            print(comments_amount)
            if a < comments_amount and comments[-1]['is_operator']:
                break
            await asyncio.sleep(10)

        return self._parse_html(
            html_string=comments[-1]['body']) if comments else None

    @staticmethod
    def _parse_html(html_string: str) -> str:
        soup = BeautifulSoup(html_string, 'html.parser')
        return soup.get_text(strip=True)

    @staticmethod
    def _get_doc_link(attachment: dict) -> str:
        return attachment['doc']['url']

    @staticmethod
    def _get_photo_link(attachment: dict) -> str:
        return attachment['photo']['sizes'][-1]['url']

    def process_attachments(self):
        for attachment in self.attachments:
            if attachment['type'] == 'photo':
                processed_attachment = self._get_photo_link(attachment)
                self.processed_attachments.append(processed_attachment)
            elif attachment['type'] == 'doc':
                processed_attachment = self._get_doc_link(attachment)
                self.processed_attachments.append(processed_attachment)

    def _create_richpannel_message(self):
        return self.text + '\n\n' + '\n\n'.join(self.processed_attachments)
