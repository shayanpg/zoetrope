from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def is_https_url(message):
    return message[:5] == 'https'
