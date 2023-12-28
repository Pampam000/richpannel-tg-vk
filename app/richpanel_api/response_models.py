from pydantic import BaseModel, HttpUrl


class Comment(BaseModel):
    attachments: list[str] = []
    author_id: str = ''
    created_at: str
    body: str
    html_body: str
    id: str
    metadata: dict = {}
    plain_body: str
    type: str = 'Comment'
    via: dict = {}
    is_operator: bool = True

class SourceParam(BaseModel):
    address: str
class Source(BaseModel):
    from_: SourceParam
    to: SourceParam


class Via(BaseModel):
    channel: str
    source: Source


class CustomFields(BaseModel):
    pass  # Add fields as needed


class Ticket(BaseModel):
    id: str
    cookieId: str
    created_at: str
    updated_at: str
    assignee_id: str
    organization_id: str
    priority: str
    recipient: str
    status: str
    subject: str
    via: Via
    comments: list[Comment]
    url: HttpUrl
    satisfaction_rating: dict = {}
    tags: list[str]
    scenarioName: str | None = None
    customFields: CustomFields = {}

class TicketResponse(BaseModel):
    ticket: Ticket
