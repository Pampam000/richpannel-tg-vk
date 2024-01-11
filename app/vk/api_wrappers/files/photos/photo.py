from aiohttp import ClientResponse

from app.vk.api_wrappers.files.file import File


class Photo(File):
    url = "photos"
    save_method = ".saveMessagesPhoto"
    form_data_field_name = "photo"

    async def _save(self, data: dict):
        response: ClientResponse = await self._request(
            method="GET",
            url=self.url + f"{self.save_method}",
            params={
                'v': self.api_version,
                'photo': data['photo'],
                'server': data['server'],
                'hash': data['hash'],
            }
        )
        response: dict = await response.json()
        response: dict = response['response'][0]
        return f'photo{response["owner_id"]}_{response["id"]}'
