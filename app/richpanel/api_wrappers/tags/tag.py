from ..base.base_wrapper import BaseRichpannelWrapper


class Tag(BaseRichpannelWrapper):
    url = "tags"

    async def get_tags(self) -> dict:
        return await self._request(method="GET", url=self.url)

    async def get_tag_id_by_name(self, name: str) -> str:
        tags: dict = await self.get_tags()
        tags: list[dict] = tags['tag']

        for tag in tags:
            if tag['name'] == name:
                return tag['id']
        return ''
