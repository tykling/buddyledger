from django import template

@register.filter
def keyvalue(dict, key):    
    return dict[key]