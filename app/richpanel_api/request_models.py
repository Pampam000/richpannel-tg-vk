from pydantic import BaseModel

from . import enums


class Base(BaseModel):
    class Config:
        use_enum_values = True


class Comment(Base):
    id: str | None = None
    body: str
    sender_type: enums.CommentSenderType


class SourceParam(Base):

    name: str | None = None


class From(SourceParam):
    address: str


class To(SourceParam):
    address: str | None = None


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
    tags: list[str] | None = None
    subject: str | None = None


class TicketRequest(Base):
    ticket: Ticket
