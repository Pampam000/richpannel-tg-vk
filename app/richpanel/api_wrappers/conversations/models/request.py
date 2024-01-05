from . import enums
from ...base.models.request import Base, RetrieveByField
from ...customers.models.request import Customer


class Comment(Base):
    id: str | None = None
    body: str
    sender_type: enums.CommentSenderType


class From(Customer):
    pass


class To(Customer):
    pass


class Source(Base):
    from_: From
    to: To | None = None


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


__all__ = [
    "Comment",
    "From",
    "To",
    "Source",
    "Via",
    "Ticket",
    "UpdateTicket",
    "TicketRequest",
    "RetrieveByField",
]
