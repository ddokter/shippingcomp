from django import forms
from django.apps import apps
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from payments import RedirectNeeded
from djbosui.views.base import CreateView, DetailView, UpdateView, DeleteView
from ..models.contact import Contact
from ..models.order import Order
from ..cart import get_cart


class OrderContact(CreateView):

    """ Add contact to order. The order itself is also created. """

    @property
    def model(self):

        """ Override to get model from kwargs """

        _model = apps.get_model(settings.SC_CONTACT_MODEL)

        return _model

    def create_order(self, contact):

        """Create order using contact. The order is filled with cart
        items."""

        order = Order(contact=contact)
        order.save()

        cart = get_cart(self.request)

        for item in cart.list_items():
            order.orderitem_set.update_or_create(
                product=item["product"],
                quantity=item["quantity"])

        return order

    def form_valid(self, form):

        self.object = form.save()

        self.order = self.create_order(self.object)

        # When the order has been successfully created, it is now time to
        # emtpy the cart.
        #
        get_cart(self.request).clear()

        return HttpResponseRedirect(self.get_success_url())

    @property
    def success_url(self):

        return reverse("order_review", kwargs={'pk': self.order.id})

    @property
    def action_url(self):

        return reverse("order_add_contact")

    @property
    def cancel_url(self):

        return reverse("cart")


class OrderReview(DetailView):

    """ Show the complete order """

    model = Order
    template_name = "order_review.html"


class OrderCancel(DeleteView):

    """ Delete the order, with the usual confirm """

    model = Order
    success_url = reverse_lazy("index")


class OrderPayment(DetailView):

    """Take the customer to the external payment, whatever is
    configured through django_payments"""

    model = Order
    template_name = "order_payment.html"

    def get(self, request, *args, **kwargs):

        """ Get the payment provider's form, or redirect to the
        provided URL. The payment is created if need be. """

        self.object = self.get_object()

        self.payment = self.object.get_payment()

        try:
            form = self.payment.get_form(data=request.POST or None)
        except RedirectNeeded as redirect_to:
            return HttpResponseRedirect(str(redirect_to))

        context = self.get_context_data(object=self.object, form=form)

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):

        return self.get(request, *args, **kwargs)
