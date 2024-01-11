import asyncio

from aiogram.types import Message

from app import config as cf
from app import db
from app.create_instances import richpannel_api, bot
from app.logger import logger
from app.task import check_second_operator_answer, pop_task
from app.tg_bot import utils


class TGRichpanelConnector:
    def __init__(self, message: Message):
        self.message = message
        user = message.from_user
        self.user_id = str(user.id)
        self.user_fullname = user.full_name
        self.text = ''
        if message.text:
            self.text = message.text
        self.attachment = None
        self.processed_attachment = None
        self.ticket_id: str | None = None
        logger.debug(f'{self.user_id} sent message(text={self.text}'
                     f'attachment={self.attachment}')

    async def _create_attachment_from_tg_file(self, file_id: str) -> None:
        file = await bot.get_file(file_id=file_id)
        self.attachment = f"https://api.telegram.org/file/bot" \
                          f"{cf.BOT_TOKEN}/{file.file_path}"

    async def process_attachment(self):
        if not (
                self.message.photo or self.message.document or self.message.video):
            return

        if self.message.caption:
            self.text = self.message.caption

        if self.message.photo:
            file_id: str = self.message.photo[-1].file_id
            await self._create_attachment_from_tg_file(file_id=file_id)

        elif self.message.document:
            file_id: str = self.message.document.file_id
            await self._create_attachment_from_tg_file(file_id=file_id)

        elif self.message.video:
            file_id: str = self.message.video.file_id
            await self._create_attachment_from_tg_file(file_id=file_id)

    async def process_message(self):
        await self.process_attachment()
        customer_response = await richpannel_api.customer.create_customer(
            email=self.user_id,
            name=self.user_fullname,
        )
        logger.debug(f'{self.user_id} got customer_response='
                     f'{customer_response}')
        if 'error' in customer_response:
            logger.debug(f'{self.user_id} customer already exists')
            self.ticket_id = await db.get_customer_ticket_id(
                email=self.user_id
            )
            logger.debug(f'TG:{self.user_id} - ticket_id={self.ticket_id}')
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
        logger.debug(f'{self.user_id} got an update response = '
                     f'{update_response}')
        await self._send_message(response=update_response, check=True)

    async def _send_message_if_ticket_is_closed(self):
        message_response, self.ticket_id = await \
            self._get_message_response_and_ticket_id()
        logger.debug(f'{self.user_id} got a message_response = '
                     f'{message_response}')
        logger.debug(f'{self.user_id} got a ticket_id = {self.ticket_id}')
        await db.update_customer_ticket_id(
            email=self.user_id,
            ticket_id=self.ticket_id
        )
        logger.debug(f'{self.user_id} updated ticket_id in db')
        await self._send_message(response=message_response)

    async def _send_message_if_no_ticket(self):
        message_response, self.ticket_id = await \
            self._get_message_response_and_ticket_id()
        logger.debug(f'TG:{self.user_id} got a message_response='
                     f'{message_response} and ticket_id={self.ticket_id}')
        await db.create_customer(
            email=self.user_id,
            messenger_id=2,
            ticket_id=self.ticket_id
        )
        logger.debug(f'{self.user_id} created new instance in db')
        await self._send_message(response=message_response)

    def _create_richpannel_message(self) -> str:
        return self.text + f'\n\n{self.attachment}' if self.attachment else \
            self.text

    async def _check_if_answer_is_needed(self, ticket_id: str) -> bool:
        retrieve_response = await richpannel_api.conversation.retrieve_ticket(
            ticket_id=ticket_id
        )
        logger.debug(
            f'{self.user_id} retrieved ticket = {retrieve_response}')

        comments = retrieve_response['ticket']['comments']
        if len(comments) < 2:
            return True

        return not (comments[-1]['is_operator'] or comments[-2]['is_operator'])

    async def _send_message(self, response: dict, check: bool = False):
        pop_task(ticket_id=self.ticket_id)
        comments_amount = len(response['ticket']['comments'])
        logger.debug(f'{self.user_id} got comments_amount='
                     f'{comments_amount}')

        if check and await self._check_if_answer_is_needed(
                ticket_id=response['ticket']['id']
        ):
            logger.debug(f'TG:{self.user_id} answer is not needed')
            return
        operator_message, attachments = await (
            self._check_operator_answer(
                comments_amount=comments_amount,
                ticket_id=self.ticket_id
            ))
        logger.debug(f'{self.user_id} got operator_message = '
                     f'{operator_message}')
        logger.debug(f'{self.user_id} got attachments = {attachments}')
        await utils.send_operator_message(
            user_id=self.user_id,
            operator_message=operator_message,
            attachments=attachments,
        )

        await check_second_operator_answer(
            ticket_id=self.ticket_id,
            sleep_time=30,
            service_name='tg',
            user_id=self.user_id
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
            logger.debug(f'TG:{self.user_id} IT IS NORMAL IF ERROR IN '
                         f'RESPONSE!!!!')
            logger.debug(f'TG:{self.user_id} retrieved ticket = {response}')
            if 'error' in response:
                logger.debug(f'TG:{self.user_id} ticket is not created yet')
                await asyncio.sleep(10)
                continue

            if response['ticket']['status'] == "CLOSED":
                await db.unset_customer_ticket_id(email=self.user_id)
                raise TypeError('!!!TICKET CLOSED!!!')
            comments = response['ticket']['comments']
            comments_amount = len(comments)

            if a < comments_amount and comments[-1]['is_operator']:
                break
            await asyncio.sleep(10)

        return comments[-1]['body'], comments[-1]['attachments']  # if
