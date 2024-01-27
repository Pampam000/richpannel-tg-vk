from bs4 import BeautifulSoup

from app.create_instances import vk_api, richpannel_api
from app.logger import logger
from app import config as cf


async def send_operator_message(
        user_id: str,
        operator_message: str,
        attachments: list[str],
        first_comment: str,

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
            processed_attachment: str = await vk_api.document.upload(
                **request_kwargs
            )
        elif extension in cf.PHOTO_EXTENSIONS:
            request_kwargs.pop('peer_id')
            processed_attachment: str = await vk_api.photo_comment.upload(
                **request_kwargs
            )
        elif extension in cf.VIDEO_EXTENSIONS:
            processed_attachment: str = await vk_api.video.upload(
                **request_kwargs
            )
        if not processed_attachment:
            continue
        processed_attachments.append(processed_attachment)
        logger.debug(f'{user_id} has processed attachment = '
                     f'{processed_attachment}')

    logger.debug(f'first_comment = {first_comment}')
    underscore_index = first_comment.index('_')
    logger.debug(f'underscore index = {underscore_index}')


    l = 0
    for num, digit in enumerate(first_comment[underscore_index + 1:]):
        if not digit.isdigit():
            l = num + 1
            break
    post_id = first_comment[underscore_index + 1: underscore_index + l]
    logger.debug(f' post id = {post_id}')
    reply_id = first_comment.split('=')[-1]
    logger.debug(f'reply id = {reply_id}')
    gr_id = first_comment.split('wall')[1]
    group_id = ''
    for symbol in gr_id:
        if symbol.isdigit() or symbol == '-':
            group_id += symbol
        else:
            break
    logger.debug(f'group_id = {group_id}')
    while processed_attachments or text:
        comment_response = await vk_api.wall.comment(
            owner_id=group_id,
            post_id=post_id,
            reply_to_comment=reply_id,
            attachments=','.join(processed_attachments),
            message=text
        )
        logger.debug(f'comment response = {comment_response}')
        text = None
        processed_attachments = processed_attachments[10:]


def _parse_html(html_string: str) -> str:
    soup = BeautifulSoup(html_string, 'html.parser')
    return soup.get_text(strip=True)
