from pydantic import BaseModel

from app.richpanel.api_wrappers.base.models import enums


class Base(BaseModel):
    class Config:
        use_enum_values = True





class RetrieveByField(Base):
    by: enums.RetrieveByFieldType
    value: str



