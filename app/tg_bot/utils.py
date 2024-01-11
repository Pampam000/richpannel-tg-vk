from aiogram.types import BufferedInputFile
from aiogram.utils.media_group import MediaGroupBuilder
from bs4 import BeautifulSoup

from app import config as cf
from app.create_instances import bot, richpannel_api
from app.logger import logger


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
    logger.debug(f'TG:{user_id} has a text = {text}')

    if not attachments:
        logger.debug(f'TG:{user_id} sending message')
        if text:
            await bot.send_message(
                chat_id=user_id,
                text=text,
            )
        return

    media_group = MediaGroupBuilder(caption=text if text else None)
    document_media_group = MediaGroupBuilder()
    media_groups = []
    document_media_groups = []

    for num, attachment in enumerate(attachments):
        bytes_obj, extension = await richpannel_api.download.file(
            url=attachment
        )
        input_file = BufferedInputFile(
            file=bytes_obj,
            filename=f'1.{extension}',
        )
        if extension in cf.DOCUMENT_EXTENSIONS:
            logger.debug(f'TG:{user_id} adding doc to media group')
            if len(document_media_group._media) == 10:
                document_media_group = MediaGroupBuilder()
                document_media_groups.append(document_media_group)
            document_media_group.add_document(media=input_file)

        elif extension in cf.PHOTO_EXTENSIONS:
            logger.debug(f'TG:{user_id} adding photo to media group')

            if len(media_group._media) == 10:
                media_groups.append(media_group)
                media_group = MediaGroupBuilder()
            media_group.add_photo(
                media=input_file
            )
        elif extension in cf.VIDEO_EXTENSIONS:
            logger.debug(f'TG:{user_id} adding video to media group')

            if len(media_group._media) == 10:
                media_groups.append(media_group)
                media_group = MediaGroupBuilder()
            media_group.add_video(media=input_file)

    if document_media_group not in document_media_groups:
        if len(document_media_group._media):
            document_media_groups.append(document_media_group)

    if media_group not in media_groups:
        if len(media_group._media):
            media_groups.append(media_group)

    send_caption = False

    if media_groups:
        send_caption = True
        for media_group in media_groups:
            logger.debug(f'TG:{user_id} sending media group')
            await bot.send_media_group(
                chat_id=user_id,
                media=media_group.build()
            )
    if document_media_groups:
        for num, media_group in enumerate(document_media_groups):
            if not send_caption and num == 0:
                media_group.caption = text if text else None
            logger.debug(f'TG:{user_id} sending doc media group')
            await bot.send_media_group(
                chat_id=user_id,
                media=media_group.build()
            )


def _parse_html(html_string: str) -> str:
    soup = BeautifulSoup(html_string, 'html.parser')
    return soup.get_text(strip=True)
