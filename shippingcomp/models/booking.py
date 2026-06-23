from datetime import datetime
from sqids import Sqids
from django.db import models
from django.db.models import Sum, Q
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from payments.models import PaymentStatus


BOOKING_STATUS_OPTION = 0
BOOKING_STATUS_CONFIRMED = 1
BOOKING_STATUS_ONHOLD = 2
BOOKING_STATUS_CANCELLED = -1

BOOKING_STATUS_VOCAB = [(BOOKING_STATUS_OPTION, _("Option")),
                        (BOOKING_STATUS_CONFIRMED, _("Confirmed")),
                        (BOOKING_STATUS_ONHOLD, _("On hold")),
                        (BOOKING_STATUS_CANCELLED, _("Cancelled"))]


class Booking(models.Model):

    """Represent a booking for a customer on one specific cruise. The
    booking consists of a list of actual products for that cruise,
    i.e. a hut or a berth, etc.

    When payment is involved, an order can be attached to the booking,
    holding payment information.

    """

    order = models.ForeignKey("Order", null=True, blank=True,
                              on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(
        _("Status"), default=0, choices=BOOKING_STATUS_VOCAB)
    notes = models.TextField(_("Notes"), null=True, blank=True)
    contact = models.ForeignKey(settings.SC_CONTACT_MODEL,
                                on_delete=models.CASCADE)
    cruise = models.ForeignKey("Cruise", on_delete=models.CASCADE)
    pax = models.SmallIntegerField(default=1)

    @property
    def ref(self):

        return Sqids().encode([self.id, self.cruise.id, self.contact.id])

    def list_bookingproducts(self):

        return self.bookingproduct_set.all()

    def get_total(self):

        """ Return total of all prices """

        total = 0

        for product in self.list_bookingproducts():

            total += product.quantity * product.price

        for coupon in self.coupon_set.all():

            total = coupon.apply(total)

        return total

    def has_valid_coupons(self):

        return self.list_valid_coupons().exists()

    def list_valid_coupons(self):

        """ List all coupons that may be applied to this booking """

        now = datetime.now()

        return (self.contact.list_coupons().
                filter(Q(expires__isnull=True) | Q(expires__gt=now)).
                exclude(id__in=[c.id for c in self.coupon_set.all()]))

    def get_paid(self):

        """ If a payment has been made and is confirmed, show the amount """

        if getattr(self, "order", None):
            if getattr(self.order, "payment", None):
                if self.order.payment.status == PaymentStatus.CONFIRMED:
                    return self.order.payment.total

        return 0

    def get_balance(self):

        return self.get_total() - float(self.get_paid())

    def __str__(self):

        return f"Booking {self.ref} - {self.contact}"

    class Meta:

        ordering = ["contact__name"]
        app_label = "shippingcomp"
