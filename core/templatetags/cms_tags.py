import re

from bs4 import BeautifulSoup

from django import template
from django.utils.text import slugify, mark_safe


register = template.Library()


def build_anchor_id(element):
    return slugify(get_label(element) + '-section')


def get_label(element):
    return re.sub(r'^.* \- ', '', element.contents[0])


@register.filter
def add_anchors(value):
    soup = BeautifulSoup(value, 'html.parser')
    for element in soup.findAll('h2'):
        element.attrs['id'] = build_anchor_id(element)
    return mark_safe(str(soup))


@register.filter
def add_export_elements_classes(value):
    soup = BeautifulSoup(value, 'html.parser')
    mapping = [
        ('h1', 'heading-xlarge'),
        ('h2', 'heading-large'),
        ('h3', 'heading-medium'),
        ('ul', 'list list-bullet'),
        ('ol', 'list list-number'),
    ]
    for tag_name, class_name in mapping:
        for element in soup.findAll(tag_name):
            element.attrs['class'] = class_name
    return mark_safe(str(soup))
