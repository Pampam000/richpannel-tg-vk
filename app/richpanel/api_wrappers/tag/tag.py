from ..base.base_wrapper import BaseWrapper


class Tag(BaseWrapper):
    url = "tags"

    async def get_tags(self):
        response: dict = await self._request(
            method="GET",
            url=self.url
        )
        print(88, response)
        return response

    async def get_tag_id_by_name(self, name: str) -> str:
        tags: dict = await self.get_tags()
        tags: list[dict] = tags['tag']

        for tag in tags:
            if tag['name'] == name:
                return tag['id']

