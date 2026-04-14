from django.utils.translation import gettext_lazy as _
from django.template import Library
from django.utils.safestring import mark_safe as _mark_safe
from ..models.cruise import (STATUS_OPEN, STATUS_CLOSED, STATUS_SAILING,
                             STATUS_ARCHIVED)

register = Library()


@register.filter
def mark_safe(txt):

    return _mark_safe(txt)


@register.filter
def cruise_status(cruise):

    """ Return a tuple of the status and the needed BS display """

    status = cruise.get_status()

    if status == STATUS_OPEN:
        return [_("Open"), "success"]
    elif status == STATUS_CLOSED:
        return [_("Closed"), "danger"]
    elif status == STATUS_SAILING:
        return [_("Sailing"), "info"]
    else:
        return [_("Archived"), "light"]


@register.filter
def idx(listlike, idx):

    return listlike[idx]
