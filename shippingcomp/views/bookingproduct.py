from djbosui.views.base import InlineCreateView
from ..models.bookingproduct import BookingProduct


class BookingproductCreate(InlineCreateView):

    model = BookingProduct

    def get_form(self, form_class=None):

        form = super().get_form(form_class=form_class)

        fld = form.fields["cruiseproduct"]

        fld.queryset = fld.queryset.filter(cruise=self.parent.cruise)

        return form
