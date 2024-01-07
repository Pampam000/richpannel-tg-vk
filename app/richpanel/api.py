from app import AsyncClass

from app.config import RICHPANNEL_TOKEN, RICHPANNEL_BASE_URL
from .api_wrappers import Conversation, Customer, Tag
from .api_wrappers.downloads.download import Download


class Api(AsyncClass):
    base_url = RICHPANNEL_BASE_URL

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-richpanel-key": RICHPANNEL_TOKEN
    }

    async def __init__(self):
        await super().__init__()

        self.conversation = Conversation(self)
        self.customer = Customer(self)
        self.tag = Tag(self)
        self.download = Download(self)

