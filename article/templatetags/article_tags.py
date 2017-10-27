from django import template
from django.utils.html import mark_safe

from article import helpers


register = template.Library()


@register.simple_tag
def include_markdown(markdown_file_path):
    html = helpers.markdown_to_html(markdown_file_path)
    return mark_safe(html)


@register.filter
def time_to_read(value):
    if value <= 59:
        return 'Less than 1 minute'
    minutes = int(round(value / 60, 0))
    unit = 'min' if minutes == 1 else 'mins'
    return '{minutes} {unit}'.format(minutes=minutes, unit=unit)
