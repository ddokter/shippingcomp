from datetime import datetime
from sqids import Sqids
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


MODE_VOCAB = ((0, _("Percentage")), (1, _("Fixed amount")))


class Coupon(models.Model):

    """Coupons  are used to  give people  discounts. A coupon  may be
    once-off, but also permanent.

    """

    booking = models.ForeignKey("Booking", on_delete=models.SET_NULL,
                                blank=True, null=True)
    contact = models.ForeignKey(settings.SC_CONTACT_MODEL,
                                on_delete=models.CASCADE)
    amount = models.FloatField(verbose_name=_('Amount'))
    mode = models.SmallIntegerField(choices=MODE_VOCAB)
    created = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField(blank=True, null=True)
    used = models.BooleanField(default=False)

    @property
    def code(self):

        return Sqids().encode([self.id,
                               self.created.hour,
                               self.created.minute,
                               self.created.second])

    def is_valid(self, booking):

        """ Check validity if the coupon has an expiry date """

        if booking.contact != self.contact:
            return False
        
        if self.expires:
            return self.expires > datetime.now()
        else:
            return True

    def discount(self):

        """ Show the discount for this coupon """

        if self.mode == 0:
            return f"{self.amount}%"            
        else:
            return f"{self.amount}"

    def apply(self, amount):

        """ Apply the coupon to the amount """

        if self.mode == 0:

            return (self.amount / 100) * float(amount)

        else:

            return float(amount) - self.amount

    def __str__(self):

        return self.code
        
    class Meta:

        app_label = "shippingcomp"
