from decimal import Decimal
from sqids import Sqids
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from .booking import Booking
from .payment import Payment


TAX = 1.09


class OrderManager(models.Manager):

    def by_ref(self, ref):

        sqids = Sqids()

        (order_id, contact_id, payment_id) = sqids.decode(ref)

        return self.filter(id=order_id, contact__id=contact_id,
                           payment__id=payment_id)


class Order(models.Model):

    """Order for a single user, consisting of order items. Payment is
    done using an external partner (i.e. Mollie), so we need to store
    the payment ID.

    """

    objects = OrderManager()

    date = models.DateTimeField(auto_now_add=True)
    contact = models.ForeignKey(settings.SC_CONTACT_MODEL,
                                on_delete=models.CASCADE)
    payment = models.OneToOneField("Payment", on_delete=models.CASCADE,
                                   null=True, blank=True)

    def __str__(self):

        return f"Order {self.ref} - {self.contact}"

    @property
    def ref(self):

        if not self.payment:

            return f"#{str(self.id).zfill(8)}"
        
        sqids = Sqids()

        return sqids.encode([self.id, self.contact.id, self.payment.id])

    def get_status(self):

        """ Retrieve status from payment API """

        if not self.payment:
            return "preinit"
        else:
            return self.get_payment().status

    def list_cruises(self):

        """ List all separate cruises for this order """

        cruises = []

        for item in self.orderitem_set.all():

            if not item.product.cruise in cruises:
                cruises.append(item.product.cruise)

        return cruises

    def create_bookings(self):

        """Create the bookings for the order. This loops through the
        distinct cruises and creates bookings accordingly. Per
        booking, products will be added that are attached to this
        order as orderitems.

        """

        if self.booking_set.exists():
            return None

        for cruise in self.list_cruises():

            booking = Booking.objects.create(order=self,
                cruise=cruise, contact = self.contact)

            for item in self.list_orderitems().filter(
                    product__cruise=cruise):

                booking.bookingproduct_set.create(
                    cruiseproduct=item.product,
                    price=item.price,
                    quantity=item.quantity)

    def list_bookings(self):

        return self.booking_set.all()

    def list_orderitems(self):

        return self.orderitem_set.all()

    def get_total_price(self):

        return sum(item.price * item.quantity
                   for item in self.list_orderitems())

    def get_total_tax(self):

        return self.get_total_price() / TAX

    def get_payment(self):

        """ Get or create the payment for this order """

        if not self.payment:
            payment = Payment.objects.create(
                variant='mollie',
                description=str(self),
                total=Decimal(self.get_total_price()),
                tax=Decimal(self.get_total_tax()),
                currency='EUR'
            )

            self.payment = payment
            self.save()

        return self.payment

    class Meta:

        app_label = "shippingcomp"
