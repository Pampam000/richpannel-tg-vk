from .models.response import UserModel
from ..base.base_wrapper import BaseVkWrapper


class User(BaseVkWrapper):
    url = "users"

    async def get_user_by_id(self, user_id: str) -> UserModel:
        response: dict = await self._request(
            method="GET",
            url=self.url + f'.get',
            params={
                'v': self.api_version,
                'user_ids': user_id
            }
        )

        return UserModel(**response['response'][0])
