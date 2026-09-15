from django.utils.translation import gettext_lazy as _
from django.template import Library
from django.utils.safestring import mark_safe as _mark_safe
from ..models.cruise import STATUS


register = Library()


@register.filter
def mark_safe(txt):

    return _mark_safe(txt)


@register.filter
def cruise_status(cruise):

    """ Return a tuple of the status and the needed BS display """

    return STATUS.as_display(cruise.get_status())


@register.filter
def idx(listlike, idx):

    return listlike[idx]
