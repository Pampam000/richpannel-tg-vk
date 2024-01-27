from aiohttp import ClientResponse

from app import config as cf
from app.logger import logger
from app.vk.api_wrappers.files.file import File


class PhotoComment(File):
    url = 'photos'
    save_method = '.saveWallPhoto'
    form_data_field_name = "photo"
    upload_method = '.getWallUploadServer'

    async def _save(self, data: dict):
        response: ClientResponse = await self._request(
            method="GET",
            url=self.url + f"{self.save_method}",
            params={
                'v': self.api_version,
                'photo': data['photo'],
                'server': data['server'],
                'hash': data['hash'],
            },
            headers={'authorization': f'Bearer {cf.VK_USER_TOKEN}'}
        )
        response: dict = await response.json()
        response: dict = response['response'][0]
        logger.debug(f'response = {response}')
        return f'photo{response["owner_id"]}_{response["id"]}'

    async def _get_upload_url(self, peer_id: str | int | None = None):
        response: ClientResponse = await self._request(
            method='GET',
            url=self.url + self.upload_method,
            params={
                'v': self.api_version,
            },
            headers={'authorization': f'Bearer {cf.VK_USER_TOKEN}'}
        )
        response: dict = await response.json()
        return response['response']['upload_url']
