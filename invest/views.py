from django.conf import settings
from django.http import Http404
from django.views.generic.edit import FormView

from invest import forms


class FeatureFlagMixin:
    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_FLAGS['HIGH_POTENTIAL_OPPORTUNITIES_ON']:
            raise Http404()
        return super().dispatch(*args, **kwargs)


class HighPotentialOpportunityFormView(FeatureFlagMixin, FormView):
    template_name = 'invest/high-potential-opportunities-form.html'
    form_class = forms.HighPotentialOpportunityForm

    #  TODO TT-364: 404 if the opportunity_slug is invalid
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # TODO TT-364: retrieve from CMS
        kwargs['field_attributes'] = {
            'full_name': {
                'label': 'Your name',
            },
            'role_in_company': {
                'label': 'Position in company'
            }
        }
        return kwargs

    def form_valid(self, form):
        # TODO T-336: link to thank you page
        # TODO TT-337: send email confirmation via govnotify and forms api
        return super().form_valid()
