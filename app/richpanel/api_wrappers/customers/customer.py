from .models import CustomerRequest, RetrieveByField, Customer as _Customer
from ..base.base_wrapper import BaseRichpannelWrapper


class Customer(BaseRichpannelWrapper):
    url = "customers"

    async def create_customer(self, **kwargs) -> dict:
        return await self._create_customer(
            CustomerRequest(customer=_Customer(**kwargs))
        )

    async def _create_customer(self, customer: CustomerRequest) -> dict:
        response: dict = await self._request(
            method="POST",
            url=self.url,
            json=customer.model_dump(exclude_none=True)
        )

        return response

    """async def fetch_customer_from_email_or_phone(
            self, by: str, value: str) -> dict:
        return await self._fetch_customer_from_email_or_phone(
            customers=RetrieveByField(by=by, value=value)
        )"""

    async def fetch_customer_from_email_or_phone(
            self, customer: RetrieveByField) -> dict:
        response: dict = await self._request(
            method="GET",
            url=self.url + f'/{customer.by}/{customer.value}'
        )
        return response
