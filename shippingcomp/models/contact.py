from django.db import models
from django.utils.translation import gettext_lazy as _


class Contact(models.Model):

    """Single user details.
    """

    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15, null=True, blank=True)
    zipcode = models.CharField(_("Zipcode"), null=True, blank=True,
                               max_length=7)
    address = models.TextField(_("Address"), null=True, blank=True)
    city = models.CharField(_("City"), max_length=100, null=True, blank=True)

    def __str__(self):

        return self.email

    class Meta:

        app_label = "shippingcomp"
        swappable = "SC_CONTACT_MODEL"
