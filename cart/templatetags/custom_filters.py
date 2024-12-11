from django import template

register=template.Library()   # one library object helps us to 

@register.filter()
def multiply(v1,v2):
    return v1*v2

