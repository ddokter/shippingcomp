from django.views.generic import TemplateView
from .calendar import Calendar
from ..models.cruise import Cruise


class Home(TemplateView, Calendar):

    """The index view provides a yearly overview of cruises.

    """
    
    template_name = "index.html"

    def get_data(self):

        """ Show data for calendar. This may generate tasks on the fly, for
        repeated scheduled tasks."""

        data = {}

        for day in self.month['days']:

            data[day] = Cruise.objects.filter(from_date__lte=day,
                                              to_date__gte=day).exists()

        return data
