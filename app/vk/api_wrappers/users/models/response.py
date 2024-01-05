from pydantic import BaseModel


class UserModel(BaseModel):
    id: int
    first_name: str
    last_name: str
