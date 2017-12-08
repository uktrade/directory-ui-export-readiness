from django.template.loader import render_to_string

import pytest


@pytest.mark.parametrize('template_name', (
    '400.html',
    '403.html',
    '404.html',
))
def test_error_templates(template_name):
    assert render_to_string(template_name, {})
