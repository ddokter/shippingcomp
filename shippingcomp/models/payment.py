from decimal import Decimal
from json import loads
from django.db import models
from django.conf import settings
from django.urls import reverse, reverse_lazy
from payments import PurchasedItem
from payments.models import BasePayment


class Payment(BasePayment):

    """ShippingComp payment implementation to take care of correct
    URL handling. Payments are bound to orders in a one-to-one
    relationship, so self.order refers to the connected order.

    """

    def __str__(self):

        if getattr(self, "order", None):
            return f"{self.order}: {self.total} [{self.status}]"
        else:
            return (f"{self.id} {self.get_consumer_name()}"
                    f" {self.get_consumer_account()}:"
                    f" {self.total} [{self.status}]")

    def get_failure_url(self):

        return reverse("payment_failure", kwargs={'pk': self.order.id})

    def get_success_url(self):

        return reverse("payment_success", kwargs={'pk': self.order.id})

    def get_purchased_items(self):

        for item in self.order.list_orderitems():
            yield PurchasedItem(
                name=str(item.product),
                sku=item.sku,
                quantity=item.quantity,
                price=item.price,
                currency='EUR',
            )

    def get_extra_data(self):

        return loads(self.extra_data)

    def get_consumer_name(self):

        try:
            return self.get_extra_data()["details"]["consumerName"]
        except KeyError:
            return "Unknown"

    def get_consumer_account(self):

        try:
            return self.get_extra_data()["details"]["consumerAccount"]
        except KeyError:
            return "Unknown"
