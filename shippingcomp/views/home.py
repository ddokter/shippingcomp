from django.views.generic import TemplateView
from ..cart import get_cart


class Home(TemplateView):

    template_name = "index.html"
