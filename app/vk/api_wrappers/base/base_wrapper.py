from typing import TYPE_CHECKING

from app.base_wrapper import BaseWrapper

if TYPE_CHECKING:
    from app.vk import Api

from app import config as cf


class BaseVkWrapper(BaseWrapper):
    api_version = cf.VK_API_VERSION

    def __init__(self, api: "Api"):
        super().__init__(api=api)
        self.base_url: str = cf.VK_BASE_URL
