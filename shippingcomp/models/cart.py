from django.db import models
from django.utils.translation import gettext_lazy as _


class Cart(models.Model):

    """Shopping cart, holding current items for a given user,
    previous to creating an order. Only when the cart is 'pushed' to
    checkout, is the order created. 

    """

    def total_price(self):

        return sum([item.total_price() for item in self.list_items()])

    def list_items(self):

        return self.cartitem_set.all()

    class Meta:

        app_label = "shippingcomp"
