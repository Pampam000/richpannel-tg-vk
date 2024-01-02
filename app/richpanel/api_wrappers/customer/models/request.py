from ...base.models.request import Base, RetrieveByField


class Customer(Base):
    phone: str | None = None
    email: str | None = None
    name: str | None = None
    firstName: str | None = None
    lastName: str | None = None


class CustomerRequest(Base):
    customer: Customer
