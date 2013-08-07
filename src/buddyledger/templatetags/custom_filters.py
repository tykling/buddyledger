from django import template
from django.template.defaultfilters import stringfilter
from decimal import *
register = template.Library()


@register.filter
def keyvalue(dict, key):
    return dict[key]

@register.filter
def templateabs(value):
    if value != "n/a":
        value = abs(Decimal(value))
    return value
