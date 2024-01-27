from app.create_instances import richpannel_api, vk_api
from .api_wrappers.users.models.response import UserModel
from .. import db
from ..logger import logger


class VKRichpanelConnector:
    def __init__(self, request: dict):
        self.request = request
        self.message: dict = self.request['object']['message']
        self.attachments: list = self.message['attachments']

        self.user_id = str(self.message['from_id'])
        self.text: str = self.message['text']
        self.ticket_id = None
        self.processed_attachments = []
        self._suffix = '__vk__'

    async def process_request(self):
        await self._process_attachments()
        user: UserModel = await vk_api.user.get_user_by_id(self.user_id)

        logger.debug(f'{self.user_id} sent a message with text = {self.text}')
        logger.debug(f'{self.user_id} sent a message with attachments = '
                     f'{self.attachments}')

        customer_response = await richpannel_api.customer.create_customer(
            email=self.user_id + self._suffix,
            name=user.first_name + " " + user.last_name,
        )
        logger.debug(
            f'{self.user_id}: customer_response = {customer_response}'
        )
        if 'error' in customer_response:
            logger.debug(f'{self.user_id} customer already exists')
            self.ticket_id = await db.get_customer_ticket_id(
                email=self.user_id, messenger_id=1)
            logger.debug(f'{self.user_id} - ticket_id={self.ticket_id}')
            if self.ticket_id:
                await self._send_message_if_ticket_is_open()
            else:
                await self._send_message_if_ticket_is_closed()
            return
        await self._send_message_if_no_ticket()

    async def _send_message_if_ticket_is_closed(self):
        message_response, self.ticket_id = await \
            self._get_message_response_and_ticket_id()
        logger.debug(f'{self.user_id} got a message_response = '
                     f'{message_response}')
        logger.debug(f'{self.user_id} got a ticket_id = {self.ticket_id}')
        await db.update_customer_ticket_id(
            email=self.user_id,
            ticket_id=self.ticket_id,
            messenger_id=1,
        )
        logger.debug(f'{self.user_id} updated ticket_id in db')
        # await self._send_message(response=message_response)

    async def _send_message_if_no_ticket(self):
        message_response, self.ticket_id = await \
            self._get_message_response_and_ticket_id()
        logger.debug(f'{self.user_id} got a message_response = '
                     f'{message_response}')
        logger.debug(f'{self.user_id} got a ticket_id = {self.ticket_id}')
        await db.create_customer(
            email=self.user_id,
            messenger_id=1,
            ticket_id=self.ticket_id
        )
        logger.debug(f'{self.user_id} created new instance in db')
        # await self._send_message(response=message_response)

    async def _send_message_if_ticket_is_open(self):
        update_response = await richpannel_api.conversation.update_ticket(
            ticket_id=self.ticket_id,
            message=self._create_richpannel_message()
        )
        logger.debug(f'{self.user_id} got an update response = '
                     f'{update_response}')
        # await self._send_message(response=update_response, check=True)

    async def _get_message_response_and_ticket_id(self) -> tuple:
        message_response = await richpannel_api.conversation.create_ticket(
            messenger='vkontakte',
            message=self._create_richpannel_message(),
            channel_type='email',
            address=self.user_id + self._suffix,
        )
        if message_response:
            ticket_id: str = message_response['ticket']['id']
        else:
            ticket_id = None
        return message_response, ticket_id

    @staticmethod
    def _get_doc_link(attachment: dict) -> str:
        return attachment['doc']['url']

    @staticmethod
    def _get_photo_link(attachment: dict) -> str:
        return attachment['photo']['sizes'][-1]['url']

    @staticmethod
    async def _get_video_link(attachment: dict) -> str:
        return await vk_api.video.get(
            owner_id=attachment['video']['owner_id'],
            video_id=attachment['video']['id']
        )

    @staticmethod
    def _get_sticker_link(attachment: dict) -> str:
        return attachment['sticker']['images'][-1]['url']

    async def _process_attachments(self):
        for attachment in self.attachments:
            processed_attachment = None

            if attachment['type'] == 'photo':
                processed_attachment = self._get_photo_link(attachment)
            elif attachment['type'] == 'doc':
                processed_attachment = self._get_doc_link(attachment)
            elif attachment['type'] == 'video':
                processed_attachment = await self._get_video_link(attachment)
            elif attachment['type'] == 'sticker':
                processed_attachment = self._get_sticker_link(attachment)

            if processed_attachment:
                self.processed_attachments.append(processed_attachment)

    def _create_richpannel_message(self):
        return self.text + '\n\n' + '\n\n'.join(self.processed_attachments)

    # async def _check_if_answer_is_needed(self, ticket_id: str) -> bool:
    #    retrieve_response = await richpannel_api.conversation.retrieve_ticket(
    #        ticket_id=ticket_id
    #    )
    #    logger.debug(
    #        f'{self.user_id} retrieved ticket = {retrieve_response}')
#
#    comments = retrieve_response['ticket']['comments']
#    if len(comments) < 2:
#        return True
#
#    return not (comments[-1]['is_operator'] or comments[-2]['is_operator'])
