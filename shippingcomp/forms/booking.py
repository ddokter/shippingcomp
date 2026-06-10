from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.forms.widgets import Textarea
from django.conf import settings
from ..models.booking import Booking


class BookingForm(forms.ModelForm):

    new_contact = forms.CharField()

    class Meta:
        model = Booking
        fields = '__all__'
