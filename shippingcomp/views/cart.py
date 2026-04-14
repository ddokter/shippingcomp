from django.views.generic import TemplateView
from ..cart import get_cart
from ..models.cruiseproduct import CruiseProduct


class CartView(TemplateView):

    def get_template_names(self):

        """ Override for returning a specific or the default template """

        return [self.request.POST.get("template", "cart.html")]

    def get(self, request, *args, **kwargs):

        """ Get cart. May be empty"""

        self.cart = get_cart(request)

        return super().get(request, *args, **kwargs)


class CartDeleteView(TemplateView):

    template_name = "cart.html"

    def get(self, request, *args, **kwargs):

        """ Get cart. May be empty"""

        self.cart = get_cart(request)
        self.cart.clear()

        return super().get(request, *args, **kwargs)


class CartItemView(TemplateView):

    http_method_names = ["post", "delete", "get", "put"]

    def get_template_names(self):

        """ Override for returning a specific or the default template """

        return [self.request.POST.get("template", "snippets/cartitem.html")]

    def get_context_data(self,*args, **kwargs):

        context = super().get_context_data(*args,**kwargs)

        product = get_cart(self.request).get(str(kwargs.get("pk")))
        context['product'] = product

        return context

    def post(self, request, *args, **kwargs):

        self.cart = get_cart(request)

        if kwargs.get("pk", None):
            product = CruiseProduct.objects.get(id=kwargs.get("pk"))
            self.cart.add(product, quantity=int(request.POST.get("qty", 1)))

        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):

        self.cart = get_cart(request)

        product = CruiseProduct.objects.get(id=kwargs.get("pk"))

        self.cart.remove(product)

        return super().get(request, *args, **kwargs)
