from django.views.generic import TemplateView
from django.contrib import messages
from ..cart import get_cart
from ..models.cruiseproduct import CruiseProduct


class CartProductView(TemplateView):

    template_name = "snippets/cartproduct.html"
    http_method_names = ["post", "delete", "get", "put"]
    
    def get_template_names(self):

        """ Override for returning a specific or the default template """

        return [self.request.POST.get("template", "snippets/cartproduct.html")]

    def get_context_data(self,*args, **kwargs):
        
        context = super().get_context_data(*args,**kwargs)

        if "product" in self.request.POST:
            product = CruiseProduct.objects.get(id=self.request.POST.get("product"))
        
            context['product'] = product
        elif kwargs.get("pk", None):
            product = CruiseProduct.objects.get(id=kwargs.get("pk"))
            context['product'] = product
            
        return context
    
    def post(self, request, *args, **kwargs):

        self.cart = get_cart(request)

        if kwargs.get("pk", None):
            product = CruiseProduct.objects.get(id=kwargs.get("pk"))
            self.cart.add(product, quantity=int(request.POST.get("qty", 1)))
        else:
            product = CruiseProduct.objects.get(id=request.POST.get("product"))
            self.cart.add(product)

        messages.success(request, "Product added")
            
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):

        self.cart = get_cart(request)

        product = CruiseProduct.objects.get(id=kwargs.get("pk"))

        self.cart.remove(product)

        messages.success(request, "Product removed")
        
        return super().get(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):

        self.cart = get_cart(request)

        product = CruiseProduct.objects.get(id=kwargs.get("pk"))

        qty = int(request.PUT.get('qty'))
        
        self.cart.add(product, quantity=qty)

        messages.success(request, "Product added")

        return super().get(request, *args, **kwargs)
