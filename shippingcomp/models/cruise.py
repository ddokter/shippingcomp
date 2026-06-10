from datetime import date, timedelta
from django.db import models
from django.db.models import Q
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from .ship import Ship
from .booking import BOOKING_STATUS_CONFIRMED
from .bookingproduct import BookingProduct


GROUP_TYPE_VOCAB = [(0.9, '<15'),
                    (1.0, 'Mixed'),
                    (1.2, '15-25'),
                    (0.8, '60+')]


STATUS_OPEN = 0
STATUS_CLOSED = 1
STATUS_SAILING = 2
STATUS_ARCHIVED = 3


class Cruise(models.Model):

    """ A cruise """

    name = models.CharField(_("Name"), max_length=100, blank=True, null=True)
    from_date = models.DateField()
    to_date = models.DateField()
    description = models.TextField(_("Description"), blank=True, null=True)

    ship = models.ForeignKey(Ship, on_delete=models.CASCADE,
                             blank=True, null=True)
    max_groupsize = models.SmallIntegerField(_("Maximum group size"))
    min_groupsize = models.SmallIntegerField(_("Minimal group size"))
    notes = models.TextField(_("Notes"), blank=True, null=True)
    plan = models.TextField(_("Plan"), blank=True, null=True)
    evaluation = models.TextField(_("Evaluation"), blank=True, null=True)

    product = models.ManyToManyField("Product", through="CruiseProduct")

    def __str__(self):

        try:
            period = (f"{self.from_date.strftime('%d %B %Y')} -\n"
                      f"{self.to_date.strftime('%d %B %Y')}"
                      )
        except AttributeError:
            period = ""

        return f"{self.name or ''} {period}"

    def short_str(self):

        return self.name or str(self)

    def has_products(self):

        return self.cruiseproduct_set.all().exists()

    def list_products(self):

        return self.cruiseproduct_set.all()

    def list_bookings(self):

        return self.booking_set.all()

    def get_groupsize(self):

        """ Get the number of people booked for this cruise """

        return (self.list_bookings()
                .filter(status__in=[0, 1])
                .aggregate(Sum("pax"))["pax__sum"] or 0)

    def get_fill_percentage(self):

        return (self.get_groupsize() / self.max_groupsize) * 100

    def get_places_left(self):

        return self.max_groupsize - self.get_groupsize()

    def get_status(self):

        """ Return status of cruise. """

        today = date.today()

        if today < self.from_date:
            if self.get_groupsize() < self.max_groupsize:
                return STATUS_OPEN
            else:
                return STATUS_CLOSED
        elif today < self.to_date:
            return STATUS_SAILING
        else:
            return STATUS_ARCHIVED

    class Meta:
        ordering = ["from_date", "to_date"]
        app_label = "shippingcomp"
