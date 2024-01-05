from ...base.models.request import Base, RetrieveByField


class Customer(Base):
    uid: str | None = None
    # appClientId: str | None = "699710141"
    phone: str | None = None
    address: str | None = None
    email: str | None = None
    name: str | None = None
    firstName: str | None = None
    lastName: str | None = None


class CustomerRequest(Base):
    customer: Customer


__all__ = [
    "Base",
    "RetrieveByField",
    "Customer",
    "CustomerRequest"
]
