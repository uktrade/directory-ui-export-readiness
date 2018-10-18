from django.views.generic import TemplateView
from django.utils.functional import cached_property

from directory_cms_client.client import cms_api_client
from directory_components.helpers import SocialLinkBuilder

from core.helpers import handle_cms_response
from prototype.helpers import (
    unprefix_prototype_url, prefix_international_news_url)


class GetCMSPageByFullPathMixin(TemplateView):

    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_full_path(
            full_path=unprefix_prototype_url(self.request.path),
            draft_token=self.request.GET.get('draft_token'),
        )
        return handle_cms_response(response)

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            page=self.page,
            *args,
            **kwargs
        )


class SlugFromKwargsMixin():
    @property
    def slug(self):
        return self.kwargs['slug']


class InternationalNewsCMSPageMixin(GetCMSPageByFullPathMixin):

    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_full_path(
            full_path=prefix_international_news_url(self.request.path),
            draft_token=self.request.GET.get('draft_token'),
        )
        return handle_cms_response(response)


class SocialLinksMixin():

    @cached_property
    def social_links(self):

        social_links_builder = SocialLinkBuilder(
            self.request.build_absolute_uri(),
            self.page['title'],
            'Great.gov.uk')
        return social_links_builder.links

    def get_context_data(self, *args, **kwargs):

        return super().get_context_data(
            social_links=self.social_links,
            *args,
            **kwargs
        )
