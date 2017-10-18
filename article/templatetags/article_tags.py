import markdown2

from django import template
from django.utils.html import mark_safe

from django.template.loader import render_to_string


register = template.Library()


@register.simple_tag
def include_markdown(markdown_file_path):
    html = render_to_string(markdown_file_path)
    return mark_safe(markdown2.markdown(html))
