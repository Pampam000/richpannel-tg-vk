from app import db
from app.create_instances import vk_api, richpannel_api
from app.logger import logger
from app.vk.api_wrappers.users.models.response import UserModel


class VkCommentRichpanelConnector:
    def __init__(self, request: dict):
        self.request = request
        self.object = self.request['object']
        self.attachments = self.object.get('attachments', [])
        self.processed_attachments = []
        self.text = ''

        self.comment_id = self.object['id']
        self.post_id = self.object['post_id']
        self.group_id = self.object['owner_id']
        self.user_id = str(self.object['from_id'])
        self._suffix = '__vkwall___'
        if self.user_id.startswith('-'):
            return

    async def process_request(self):
        try:
            user: UserModel = await vk_api.user.get_user_by_id(self.user_id)
        except IndexError:
            return
        logger.debug(f'user = {user}')
        await self._process_attachments()
        self.text = self.object['text']
        logger.debug(f'processed attachemnts = {self.processed_attachments}')
        logger.debug(f'self text = {self.text}')

        customer_response = await richpannel_api.customer.create_customer(
            email=self.user_id + self._suffix,
            name=user.first_name + " " + user.last_name,
        )
        logger.debug(
            f'{self.user_id}: customer_response = {customer_response}'
        )

        create_ticket = await richpannel_api.conversation.create_ticket(
            messenger='vk_wall',
            message=self._create_richpannel_message(),
            channel_type='email',
            address=self.user_id + self._suffix,
            name=user.first_name + " " + user.last_name,
        )

        logger.debug(f'{self.user_id} create ticket = {create_ticket}')

        ticket_id: str = create_ticket['ticket'][
            'id'] if create_ticket else None
        logger.debug(f'{self.user_id}: ticket_id = {ticket_id}')

        if 'error' in customer_response:
            cust_id = await db.get_customer_id(
                email=self.user_id,
                messenger_id=3,
            )
        else:
            try:
                cust_id = await db.create_customer(
                    email=self.user_id,
                    messenger_id=3,
                    ticket_id=ticket_id
                )
                logger.debug(f'cust id = {cust_id}')
            except Exception as e:
                logger.debug(f'exception = {e}')
                return


    def _create_richpannel_message(self):
        return 'https://vk.com/' + f'wall{self.group_id}_{self.post_id}?reply={self.comment_id}\n\n' + \
            self.text + '\n\n' + '\n\n'.join(self.processed_attachments)

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
