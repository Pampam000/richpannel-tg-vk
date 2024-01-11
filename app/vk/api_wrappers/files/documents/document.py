from aiohttp import ClientResponse

from ...files.file import File


class Document(File):
    url = "docs"
    save_method = '.save'
    form_data_field_name = 'file'

    async def _save(self, data: dict):
        response: ClientResponse = await self._request(
            method="GET",
            url=self.url + f"{self.save_method}",
            params={
                'v': self.api_version,
                'file': data['file'],
            }

        )
        response: dict = await response.json()

        response: dict = response['response']['doc']
        return f'doc{response["owner_id"]}_{response["id"]}'
