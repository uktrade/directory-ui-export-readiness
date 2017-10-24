from django import template
from django.contrib.humanize.templatetags import humanize

register = template.Library()


@register.filter
def intword(value):
    value = humanize.intword(value)
    if isinstance(value, int):
        # value may be so small that humanize.intword returns the input value
        return value
    return (
        value
        .replace('million', 'm')
        .replace('billion', 'bn')
        .replace('trillion', 'tn')
        .replace('.0', '')
    )
