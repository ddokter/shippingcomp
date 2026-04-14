from django.views.generic import TemplateView
from djbosui.views.base import DetailView
from ..models.order import Order


class PaymentFailure(TemplateView):

    template_name = "payment_failure.html"


class PaymentSuccess(DetailView):

    model = Order
    template_name = "payment_success.html"

    def get(self, request, *args, **kwargs):

        """Show the user that the payment succeeded and create the
        booking."""

        order = self.get_object()

        order.create_bookings()

        return super().get(request, *args, **kwargs)
