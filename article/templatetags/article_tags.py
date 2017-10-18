from django import template
from django.utils.html import mark_safe

from article import helpers


register = template.Library()


@register.simple_tag
def include_markdown(markdown_file_path):
    html = helpers.markdown_to_html(markdown_file_path)
    return mark_safe(html)
