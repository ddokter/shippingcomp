from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class OrderItem(models.Model):

    """The OrderItem consists of a product (defined by the agent) and
    a quantity.

    """

    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    product = models.ForeignKey("CruiseProduct", on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name=_('Quantity'), default=1)

    @property
    def itemnr(self):

        return "#%0.8i" % self.id

    def __str__(self):

        return f"{self.product}: {self.quantity}"

    @property
    def price(self):

        return self.product.price

    @property
    def sku(self):

        return self.product.sku

    class Meta:

        app_label = "shippingcomp"
