from django.conf import settings
from .models.cruiseproduct import CruiseProduct


def get_cart(request):

    """Initialize the cart for the session. If it is already
        there, use the cart in the session. What is in the session, is
        really just a JSON structure.

    """

    data = request.session.get(settings.CART_SESSION_ID)

    if not data:
        data = request.session[settings.CART_SESSION_ID] = {}

    return Cart(request.session, data)


class Cart:

    """The Cart class is a container of order items. It is attached
    to the user session, so a singleton per user."""

    def __init__(self, session, data):

        self.session = session
        self.data = data

    def save(self):

        """ Set modified trigger in session """

        self.session.modified = True

    def add(self, product, quantity=1):

        """
        Add product to the cart or update its quantity
        """

        if product.key not in self.data.keys():
            self.data[product.key] = {
                "id": product.id,
                "quantity": 0,
                "name": str(product),
                "price": product.price
            }

        self.data[product.key]["quantity"] += quantity

        self.save()

    def remove(self, product):

        """
        Remove a product from the cart
        """

        if product.key in self.data.keys():
            del self.data[product.key]
            self.save()

    def get(self, product_id):

        return self.data.get(product_id, None)

    def __iter__(self):

        """
        Loop through cart items and fetch the products from the database
        """

        for key in self.data.keys():

            yield {
                'id': self.data[key].get("id"),
                'name':  self.data[key].get("name", ""),
                'quantity': self.data[key]["quantity"],
                'price': self.data[key]["price"]
            }

    def list_items(self):

        for item in self:
            yield {"id": item["id"],
                   "product": CruiseProduct.objects.get(id=item["id"]),
                   "quantity": int(item["quantity"])}

    def is_empty(self):

        return len(self.data.keys()) == 0

    def nr_of_items(self):

        return sum(item["quantity"] for item in self)

    def get_total_price(self):

        """ Return total of price * quantity for all items """

        return sum(float(item["price"]) * item["quantity"]
                   for item in self)

    def clear(self):

        """ Remove cart from session """

        self.data = {}
        del self.session[settings.CART_SESSION_ID]

        self.save()
