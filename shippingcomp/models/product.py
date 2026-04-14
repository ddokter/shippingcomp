from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Product(models.Model):

    """Anything that may be ordered.

    """

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    sku = models.CharField(null=True, blank=True)

    def __str__(self):

        return self.name

    class Meta:

        app_label = "shippingcomp"
