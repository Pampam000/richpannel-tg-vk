from pydantic import BaseModel

from . import enums


class Base(BaseModel):
    class Config:
        use_enum_values = True


class Comment(Base):
    id: str
    body: str
    sender_type: enums.CommentSenderType


class SourceParam(Base):
    address: str
    name: str


class From(SourceParam):
    pass


class To(SourceParam):
    pass


class Source(Base):
    from_: From
    to: To


class Via(Base):
    channel: enums.ViaChannelType
    source: Source


class Ticket(Base):
    status: enums.TicketStatusType
    comment: Comment
    via: Via
    tags: list[str]


class TicketRequest(Base):
    ticket: Ticket
