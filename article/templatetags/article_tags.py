import dateparser

from django import template

register = template.Library()


@register.filter
def parse_date(date_string):
    if date_string:
        return dateparser.parse(date_string).strftime('%d %B %Y')
    return None
