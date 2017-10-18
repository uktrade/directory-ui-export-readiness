import markdown2

from django import template
from django.utils.html import mark_safe

from django.template.loader import render_to_string


register = template.Library()


@register.simple_tag
def include_markdown(markdown_file_path):
    html = render_to_string(markdown_file_path)
    return mark_safe(markdown2.markdown(html))


@register.simple_tag
def get_article_title(markdown_file_path):
	html = render_to_string(markdown_file_path)
	first_line = html.split('\n')[0]
	title = first_line.lstrip('# ')
	return 'Export Readiness - ' + title
