from app import AsyncClass, config as cf
from .api_wrappers.messages.message import Message
from .api_wrappers.users.user import User


class Api(AsyncClass):
    base_url = cf.VK_BASE_URL

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {cf.VK_GROUP_TOKEN}"
    }

    async def __init__(self):
        await super().__init__()

        self.user = User(self)
        self.message = Message(self)