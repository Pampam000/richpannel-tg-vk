from typing import TYPE_CHECKING

from app.base_wrapper import BaseWrapper

if TYPE_CHECKING:
    from app.richpanel import Api

from app import config as cf


class BaseRichpannelWrapper(BaseWrapper):

    def __init__(self, api: "Api"):
        super().__init__(api=api)
        self.base_url: str = cf.RICHPANNEL_BASE_URL
