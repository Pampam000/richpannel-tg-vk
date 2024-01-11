import json
from typing import Any

from aiohttp import FormData, ClientResponse

from ..base.base_wrapper import BaseVkWrapper


class File(BaseVkWrapper):
    form_data_field_name: str | None = None
    url: str | None = None
    save_method: str | None = None

    async def upload(
            self,
            peer_id: str | int,
            file: bytes,
            file_format: str
    ):
        url: str = await self._get_upload_url(peer_id=peer_id)

        data = FormData()
        data.add_field(
            name=self.form_data_field_name,
            value=file,
            filename=f'1.{file_format}')

        response: ClientResponse = await self._request(
            method="POST",
            url=url,
            data=data,
            headers={},
            use_base=False,
        )
        response: dict = json.loads(await response.text())
        return await self._save(data=response)

    async def _get_upload_url(self, peer_id: str | int):
        response: ClientResponse = await self._request(
            method='GET',
            url=self.url + f'.getMessagesUploadServer',
            params={
                'v': self.api_version,
                'peer_id': peer_id,
            },
        )
        response: dict = await response.json()
        return response['response']['upload_url']

    async def _save(self, data: dict):
        raise NotImplementedError

    @staticmethod
    async def _process_response(response: ClientResponse) -> dict | Any:
        return response
