from app import AsyncClass, config as cf
from app.vk.api_wrappers.files.documents.document import Document
from app.vk.api_wrappers.files.photos.photo import Photo
from .api_wrappers.files.videos.video import Video
from .api_wrappers.messages.message import Message
from .api_wrappers.users.user import User


class Api(AsyncClass):
    base_url = cf.VK_BASE_URL

    headers = {
        "authorization": f"Bearer {cf.VK_GROUP_TOKEN}"
    }

    async def __init__(self):
        await super().__init__()

        self.user = User(self)
        self.message = Message(self)
        self.photo = Photo(self)
        self.document = Document(self)
        self.video = Video(self)
