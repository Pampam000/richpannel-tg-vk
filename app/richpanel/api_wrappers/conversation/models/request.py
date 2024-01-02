from . import enums
from ...base.models.request import Base, RetrieveByField


class Comment(Base):
    id: str | None = None
    body: str
    sender_type: enums.CommentSenderType


class SourceParam(Base):
    id: str | None = None
    # name: str | None = None
    # firstName: str| None = None #'as'
    # lastName: str|None = None#'df'
    phone: str| None = "+79964102733"
    #address: str | None = 'test1'
    name: str | None = 'bob'
    type: str | None = 'facebook'



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
    tags: list[str]  # enums.TicketTagType
    subject: enums.TicketSubjectType


class UpdateTicket(Base):
    comment: Comment
    via: Via | None = None


class TicketRequest(Base):
    ticket: Ticket | UpdateTicket
