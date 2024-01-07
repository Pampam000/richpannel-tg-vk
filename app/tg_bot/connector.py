import asyncio

from aiogram.types import Message
from bs4 import BeautifulSoup

from app import db
from app.config import BOT_TOKEN
from app.create_instances import richpannel_api, bot


class TGRichpanelConnector:
    def __init__(self, message: Message):
        self.message = message
        self.user = message.from_user
        self.user_id = str(self.user.id)
        self.user_fullname = self.user.full_name
        self.text = message.text
        self.attachment = None
        self.processed_attachment = None
        self.ticket_id: str | None = None

    async def process_attachment(self):
        if not (self.message.photo or self.message.document):
            return
        self.text = self.message.caption
        if self.message.photo:
            file_id: str = self.message.photo[-1].file_id
            file = await bot.get_file(file_id=file_id)
            self.attachment = f"https://api.telegram.org/file/bot" \
                              f"{BOT_TOKEN}/{file.file_path}"

        if self.message.document:
            file_id: str = self.message.document.file_id
            file = await bot.get_file(file_id=file_id)
            self.attachment = f"https://api.telegram.org/file/bot" \
                              f"{BOT_TOKEN}/{file.file_path}"

    async def process_message(self):
        await self.process_attachment()
        customer_response = await richpannel_api.customer.create_customer(
            email=self.user_id,
            name=self.user_fullname,
        )
        if 'error' in customer_response:
            self.ticket_id = await db.get_customer_ticket_id(
                email=self.user_id
            )

            if self.ticket_id:
                await self._send_message_if_ticket_is_open()
            else:
                await self._send_message_if_ticket_is_closed()
            return
        await self._send_message_if_no_ticket()

    async def _send_message_if_ticket_is_open(self):
        update_response = await richpannel_api.conversation.update_ticket(
            ticket_id=self.ticket_id,
            message=self._create_richpannel_message()
        )
        await self._send_message(response=update_response)

    async def _send_message_if_ticket_is_closed(self):
        message_response, self.ticket_id = await \
            self._get_message_response_and_ticket_id()
        await db.update_customer_ticket_id(
            email=self.user_id,
            ticket_id=self.ticket_id
        )
        await self._send_message(response=message_response)

    async def _send_message_if_no_ticket(self):
        message_response, self.ticket_id = await \
            self._get_message_response_and_ticket_id()
        await db.create_customer(
            email=self.user_id,
            messenger_id=2,
            ticket_id=self.ticket_id
        )

        await self._send_message(response=message_response)

    def _create_richpannel_message(self) -> str:
        return self.text + f'\n\n{self.attachment}' if self.attachment else \
            self.text

    async def _send_message(self, response: dict):
        comments_amount = len(response['ticket']['comments'])

        operator_message, attachments = await (
            self._check_operator_answer(
                comments_amount=comments_amount,
                ticket_id=self.ticket_id
            ))
        text = None

        if operator_message:
            text = self._parse_html(operator_message)
            if 'Files Attached' in text:
                text = None

        if not attachments:
            if text:
                await self.message.answer(text=text)
            return

        for num, attachment in enumerate(attachments):
            if attachment.endswith('.pdf'):
                # if attachment[1] == 'pdf':

                await bot.send_document(
                    chat_id=self.user_id,
                    document=attachment,
                    caption=text if text and num == 0 else None
                )
            elif attachment.endswith('png') or attachment.endswith('jpg') or \
                    attachment.endswith('jpeg'):
                await bot.send_photo(
                    chat_id=self.user_id,
                    photo=attachment,
                    caption=text if text and num == 0 else None
                )

    async def _get_message_response_and_ticket_id(self):
        message_response = await richpannel_api.conversation.create_ticket(
            messenger='telegram',
            message=self._create_richpannel_message(),
            channel_type='email',
            address=self.user_id,
        )

        ticket_id: str = message_response['ticket']['id']
        return message_response, ticket_id

    async def _check_operator_answer(
            self,
            comments_amount: int,
            ticket_id: str
    ) -> tuple:
        a = comments_amount
        comments = []
        while 1:
            response = await richpannel_api.conversation.retrieve_ticket(
                ticket_id=ticket_id
            )

            if 'error' in response:
                await asyncio.sleep(10)
                continue
            comments = response['ticket']['comments']
            comments_amount = len(comments)

            if a < comments_amount and comments[-1]['is_operator']:
                break
            await asyncio.sleep(10)

        return comments[-1]['body'], comments[-1]['attachments']  # if \

    @staticmethod
    def _parse_html(html_string: str) -> str:
        soup = BeautifulSoup(html_string, 'html.parser')
        return soup.get_text(strip=True)
