from enum import Enum


class CommentSenderType(Enum):
    operator = 'operator'
    customer = 'customer'


class ViaChannelType(Enum):
    email = 'email'
    facebook_message = 'email'
    instagram = 'instagram'
    messenger = 'messenger'
    whatsapp = 'whatsapp'
    phone = 'phone'
    aircall = 'aircall'


class TicketStatusType(Enum):
    OPEN = 'OPEN'
    CLOSE = 'CLOSE'


class TicketSubjectType(Enum):
    vk = 'Вконтакте сообщения'
    tg = 'telegram'



