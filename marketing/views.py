from django.views.generic import TemplateView

from core.mixins import GetCMSPageMixin


class CampaignPageView(
    GetCMSPageMixin,
    TemplateView
):
    template_name = 'marketing/campaign.html'

    @property
    def slug(self):
        return self.kwargs['slug']
