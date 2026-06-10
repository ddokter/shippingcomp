from decimal import Decimal
from djbosui.views.base import CreateView, DetailView
from django import forms
from django.views.generic.edit import FormView
from ..models.booking import Booking
from ..models.order import Order
from ..models.payment import Payment
from ..forms.booking import BookingForm


class PaymentForm(forms.Form):

    amount = forms.FloatField()


class BookingCreate(CreateView):

    model = Booking
    form_class = BookingForm


class BookingPayment(FormView, DetailView):

    form_class = PaymentForm
    template_name = "booking_payment.html"
    model = Booking

    def form_valid(self, form):

        amount = form.cleaned_data['amount']
        booking = self.get_object()
        
        if not booking.order:

            booking.order = Order(contact=booking.contact)
            booking.save()

        if not booking.order.payment:
            payment = Payment.objects.create(
                variant="transfer",
                description="Direct payment",
                total=Decimal(amount),
                tax=Decimal(amount * 0.09),
                currency='EUR'
            )

            booking.order.payment = payment
            self.save()
        else:
            booking.order.payment.total += Decimal(amount)
            # TODO: what about tax?
            booking.order.payment.save()
            
        return super().form_valid(form)
