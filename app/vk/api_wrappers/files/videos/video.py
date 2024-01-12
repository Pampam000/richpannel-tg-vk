from aiohttp import ClientResponse

from app import config as cf
from app.vk.api_wrappers.files.file import File


class Video(File):
    url = "video"
    form_data_field_name = 'video'

    async def get(self, owner_id: str, video_id: str) -> str:
        response: ClientResponse = await self._request(
            method='GET',
            url=self.url + '.get',
            params={
                'v': self.api_version,
                'owner_id': owner_id,
                'videos': f'{owner_id}_{video_id}',
            },
            headers={'authorization': f'Bearer {cf.VK_USER_TOKEN}'}
        )
        response: dict = await response.json()
        return response['response']['items'][0]['player']

    async def _get_upload_url(self, peer_id: str | int):
        response: ClientResponse = await self._request(
            method='GET',
            url=self.url + f'.save',
            params={
                'v': self.api_version,
            },
            headers={'authorization': f'Bearer {cf.VK_USER_TOKEN}'}
        )
        response: dict = await response.json()
        return response['response']['upload_url']

    async def _save(self, data: dict):
        return f'video{data["owner_id"]}_{data["video_id"]}'
