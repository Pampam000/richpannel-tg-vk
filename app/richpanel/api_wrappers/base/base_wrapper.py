from typing import TYPE_CHECKING

from app.base_wrapper import BaseWrapper

if TYPE_CHECKING:
    from app.richpanel import Api


class BaseRichpannelWrapper(BaseWrapper):

    def __init__(self, api: "Api"):
        super().__init__(api=api)
        self.base_url = '/v1/'
