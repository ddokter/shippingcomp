from datetime import date
from djbosui.views.base import ListingView
from ..models.cruise import Cruise


class CruiseListingView(ListingView):

    model = Cruise

    def list_archived(self):

        today = date.today()

        return Cruise.objects.filter(to_date__lt=today)

    def list_planned(self):

        today = date.today()

        return Cruise.objects.filter(to_date__gte=today)
