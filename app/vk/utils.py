from bs4 import BeautifulSoup

from app.create_instances import vk_api, richpannel_api
from app.logger import logger
from app import config as cf


async def send_operator_message(
        user_id: str,
        operator_message: str,
        attachments: list[str],
):
    text = None

    if operator_message:
        text = _parse_html(operator_message)
        if 'Files Attached' in text:
            text = None
    logger.debug(f'{user_id} has a text = {text}')

    processed_attachments = []
    for attachment in attachments:
        bytes_obj, extension = await richpannel_api.download.file(
            url=attachment
        )
        processed_attachment = None
        request_kwargs = {
            'peer_id': user_id,
            'file': bytes_obj,
            'file_format': extension
        }
        if extension in cf.DOCUMENT_EXTENSIONS:
            processed_attachment: dict = await vk_api.document.upload(
                **request_kwargs
            )
        elif extension in cf.PHOTO_EXTENSIONS:
            processed_attachment: dict = await vk_api.photo.upload(
                **request_kwargs
            )
        #elif extension in cf.VIDEO_EXTENSIONS:
        #    processed_attachment: dict = await vk_api.video.upload(
        #        **request_kwargs
        #    )
        if not processed_attachment:
            continue
        processed_attachments.append(processed_attachment)
        logger.debug(f'{user_id} has processed attachment = '
                     f'{processed_attachment}')

    while processed_attachments or text:
        await vk_api.message.send(
            user_id=user_id,
            attachment=','.join(processed_attachments),
            message=text
        )
        text = None
        processed_attachments = processed_attachments[10:]



def _parse_html(html_string: str) -> str:
    soup = BeautifulSoup(html_string, 'html.parser')
    return soup.get_text(strip=True)
