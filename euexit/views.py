from django.conf import settings

from django.http import Http404

from django.views.generic.edit import FormView

from euexit import forms


class FeatureFlagMixin:
    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_FLAGS['EU_EXIT_FORMS_ON']:
            raise Http404()
        return super().dispatch(*args, **kwargs)


class InternationalContactFormView(FeatureFlagMixin, FormView):
    form_class = forms.InternationalContactForm
    template_name = 'euexit/international-contact-form.html'
