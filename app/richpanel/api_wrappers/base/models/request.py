from pydantic import BaseModel

from . import enums


class Base(BaseModel):
    class Config:
        use_enum_values = True


class RetrieveByField(Base):
    by: enums.RetrieveByFieldType
    value: str
