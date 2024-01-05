from ..base.base_wrapper import BaseVkWrapper


class Message(BaseVkWrapper):
    url = "messages"

    async def send_message(
            self,
            user_id: str,
            message: str | None = None,
            attachment: str | list[str] | None = None
    ):
        response: dict = await self._request(
            method="GET",
            url=self.url + f'.send?v={self.api_version}&user_id={user_id}&message={message}&random_id=0'
        )
        return response
