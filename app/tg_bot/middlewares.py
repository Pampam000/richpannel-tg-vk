import asyncio
from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message


class AlbumMiddleware(BaseMiddleware):
    """This middleware is for capturing media groups."""

    def __init__(self, latency: int | float = 0.01):
        """
        You can provide custom latency to make sure
        albums are handled properly in highload.
        """
        self.latency = latency
        self.album_data: dict = {}
        self.checked_media_group_id: list = []

    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any],
    ):
        if not event.media_group_id:
            return
        if not event.photo:
            return
        try:
            self.album_data[event.media_group_id].append(event.photo)

        except KeyError:
            self.album_data[event.media_group_id] = [event.photo]
            await asyncio.sleep(self.latency)

        data["album"] = self.album_data.get(event.media_group_id)
        #if not self.checked:
            #self.checked = True
        #response = await handler(event, data)
        return await handler(event, data)
        if event.media_group_id in self.album_data:
            response = await handler(event, data)
            del self.album_data[event.media_group_id]
            return response



class DocumentMiddleware(BaseMiddleware):
    """This middleware is for capturing document groups."""

    def __init__(self, latency: int | float = 0.01):
        """
        You can provide custom latency to make sure
        document groups are handled properly in highload.
        """
        self.latency = latency
        self.album_data: list = []
        self.checked: bool = False

    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any],
    ):
        if not event.document:
            return

        self.album_data.append(event.document)
        data["album"] = self.album_data
        if not self.checked:
            self.checked = True
            return await handler(event, data)
