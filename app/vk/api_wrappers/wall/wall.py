from app.vk.api_wrappers.base.base_wrapper import BaseVkWrapper


class Wall(BaseVkWrapper):
    url = 'wall'

    async def comment(
            self,
            owner_id: str | int,
            post_id: str | int,
            reply_to_comment: str | int,
            message: str | None = None,
            attachments: str | None = None,
            from_group: int = 1,
            v: str = '5.199',
    ):
        #attachments = ','.join(attachments) if attachments else None
        params = locals().copy()
        params.pop('self')
        for key, value in params.copy().items():
            if not value:
                params.pop(key)
        return await self._request(
            method='GET',
            url=self.url + '.createComment',
            params=params,
        )
