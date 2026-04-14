from django.db import models
from django.utils.translation import gettext_lazy as _


class BookingProduct(models.Model):

    """ A product for a given booking """

    booking = models.ForeignKey("Booking", on_delete=models.CASCADE)
    cruiseproduct = models.ForeignKey("CruiseProduct", on_delete=models.CASCADE)

    quantity = models.SmallIntegerField()

    @property
    def price(self):

        return self.cruiseproduct.price

    def __str__(self):

        return f"{self.booking}: {self.cruiseproduct}"
