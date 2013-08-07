from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def keyvalue(dict, key):    
    return dict[key]
    
@register.filter
def templateabs(value):
    return abs(value)