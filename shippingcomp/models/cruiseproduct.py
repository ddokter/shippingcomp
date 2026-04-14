from django.db import models
from django.db.models import Sum
from .bookingproduct import BookingProduct
from django.utils.translation import gettext_lazy as _


class CruiseProduct(models.Model):

    """A product for a given cruise. This relates base products to
    cruises with a specifief amount and price."""

    cruise = models.ForeignKey("Cruise", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    price = models.FloatField(_("Price"))
    amount = models.SmallIntegerField()

    @property
    def booked(self):

        """ Return all bookingproduct instances with this cruiseproduct """

        return BookingProduct.objects.filter(cruiseproduct=self).aggregate(
            Sum("quantity"))['quantity__sum'] or 0

    @property
    def available(self):

        """ Return actual product availability, based on initial stock
        and bookings """

        return self.amount - self.booked

    @property
    def key(self):

        """Key for the benefit of storages that need keys instead of
        id's """

        return str(self.id)

    def __str__(self):

        if self.name:
            return f"{self.name} @ {self.cruise}: {self.amount}"
        else:
            return f"{self.product} @ {self.cruise}: {self.amount}"

    def abbr(self):

        return self.name or self.product
