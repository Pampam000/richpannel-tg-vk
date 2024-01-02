from .models.request import CustomerRequest, RetrieveByField
from ..base.base_wrapper import BaseWrapper


class Customer(BaseWrapper):
    url = "customers"

    async def create_customer(self, customer: CustomerRequest):
        response = await self._request(
            method="POST",
            url=self.url,
            json=customer.model_dump()
        )

        print(55, response)
        return response

    async def fetch_customer_from_email_or_phone(self,
                                                 customer: RetrieveByField):
        response: dict = await self._request(
            method="GET",
            url=self.url + f'/{customer.by}/{customer.value}'
        )
        print(66, response)
        return response

