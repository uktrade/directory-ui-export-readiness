import pytest

from django.views.generic import TemplateView
from django.utils import translation

from core import mixins


def test_translate_non_bidi_template(rf):
    class View(mixins.TranslationsMixin, TemplateView):
        template_name_bidi = 'bidi.html'
        template_name = 'non-bidi.html'

    view = View.as_view()
    request = rf.get('/')
    request.LANGUAGE_CODE = 'en-gb'

    response = view(request)

    assert response.status_code == 200
    assert response.template_name == ['non-bidi.html']


def test_get_cms_component_mixin_is_bidi_no_cms_component(rf):
    class View(mixins.GetCMSComponentMixin, TemplateView):
        template_name = 'thing.html'
        cms_component = None

    view = View.as_view()
    request = rf.get('/')
    response = view(request)

    assert response.context_data['component_is_bidi'] is False
    assert response.context_data['cms_component'] is None


@pytest.mark.parametrize('activated_language,component_langages,expected', [
    ('en-gb', [['ar', 'Arabic']], False),
    ('en-gb', [['en-gb', 'English']], False),
    ('en-gb', [['ar', 'Arabic'], ['en-gb', 'English']], False),
    ('ar', [['ar', 'Arabic']], True),
    ('ar', [['en-gb', 'English']], False),
    ('ar', [['ar', 'Arabic'], ['en-gb', 'English']], True),
])
def test_get_cms_component_mixin_is_bidi_cms_component_not_bidi(
    rf, activated_language, component_langages, expected
):
    class View(mixins.GetCMSComponentMixin, TemplateView):
        template_name = 'thing.html'
        cms_component = {
            'meta': {
                'languages': component_langages
            }
        }

    view = View.as_view()
    request = rf.get('/')
    with translation.override(activated_language):
        response = view(request)

    assert response.context_data['component_is_bidi'] is expected
    assert response.context_data['cms_component'] == View.cms_component
