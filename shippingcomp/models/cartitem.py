from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class CartItem(models.Model):

    """The CartItem consists of a (cruise) product and a quantity.

    """

    cart = models.ForeignKey("Cart", on_delete=models.CASCADE)
    product = models.ForeignKey("CruiseProduct", on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name=_('Quantity'), default=1)

    def total_price(self):

        return self.quantity * self.product.price
        
    class Meta:

        app_label = "shippingcomp"
 
