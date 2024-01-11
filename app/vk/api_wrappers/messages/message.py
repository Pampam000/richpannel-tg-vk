from ..base.base_wrapper import BaseVkWrapper


class Message(BaseVkWrapper):
    url = "messages"

    async def send(
            self,
            user_id: str,
            message: str | None = None,
            attachment: str | list[str] | None = None
    ):
        params = {
            'v': self.api_version,
            'user_id': user_id,
            'random_id': 0
        }
        if attachment:
            if isinstance(attachment, str):
                attachment = [attachment]
            params['attachment'] = attachment

        if message:
            params['message'] = message

        response: dict = await self._request(
            method="GET",
            url=self.url + f'.send',
            params=params,
        )
        return response
