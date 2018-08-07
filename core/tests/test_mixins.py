from django.views.generic import TemplateView

from core.mixins import TranslationsMixin


def test_translate_non_bidi_template(rf):
    class View(TranslationsMixin, TemplateView):
        template_name_bidi = 'bidi.html'
        template_name = 'non-bidi.html'

    view = View.as_view()
    request = rf.get('/')
    request.LANGUAGE_CODE = 'en-gb'

    response = view(request)

    assert response.status_code == 200
    assert response.template_name == ['non-bidi.html']
