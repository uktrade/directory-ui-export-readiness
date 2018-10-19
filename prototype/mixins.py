from django.utils.functional import cached_property

from directory_cms_client.client import cms_api_client
from directory_components.helpers import SocialLinkBuilder

from core.helpers import handle_cms_response
from prototype.helpers import (
    unprefix_prototype_url, prefix_international_news_url)


class GetCMSPageByFullPathMixin():

    @property
    def cms_lookup_path(self):
        return self.request.path

    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_full_path(
            full_path=self.cms_lookup_path,
            draft_token=self.request.GET.get('draft_token'),
        )
        return handle_cms_response(response)

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            page=self.page,
            *args,
            **kwargs
        )


class GetCMSTagMixin():

    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_tag(
            tag_slug=self.slug,
            draft_token=self.request.GET.get('draft_token'),
        )
        return handle_cms_response(response)

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            tag_slug=self.slug,
            page=self.page,
            *args,
            **kwargs
        )


class PrototypeCMSLookupPath():

    @property
    def cms_lookup_path(self):
        return unprefix_prototype_url(self.request.path)


class InternationalNewsCMSLookupPath():

    @property
    def cms_lookup_path(self):
        return prefix_international_news_url(self.request.path)


class SocialLinksMixin():

    def get_context_data(self, *args, **kwargs):

        social_links_builder = SocialLinkBuilder(
            self.request.build_absolute_uri(),
            self.page['title'],
            'Great.gov.uk')

        return super().get_context_data(
            social_links=social_links_builder.links,
            *args,
            **kwargs
        )


class RelatedContentMixin():

    def get_context_data(self, *args, **kwargs):

        has_related_list_item_one = self.page['related_article_one_url'] and \
            self.page['related_article_one_title']
        has_related_list_item_two = self.page['related_article_two_url'] and \
            self.page['related_article_two_title']
        has_related_list_item_three = self.page['related_article_three_url'] \
            and self.page['related_article_three_title']

        self.page['has_related_list_item_one'] = has_related_list_item_one
        self.page['has_related_list_item_two'] = has_related_list_item_two
        self.page['has_related_list_item_three'] = has_related_list_item_three

        has_related_card_item_one = self.page['related_article_one_url'] \
            and self.page['related_article_one_title'] and \
            self.page['related_article_one_teaser']
        has_related_card_item_two = self.page['related_article_two_url'] \
            and self.page['related_article_two_title'] and \
            self.page['related_article_two_teaser']
        has_related_card_item_three = self.page['related_article_three_url'] \
            and self.page['related_article_three_title'] and \
            self.page['related_article_three_teaser']

        self.page['has_related_card_item_one'] = has_related_card_item_one
        self.page['has_related_card_item_two'] = has_related_card_item_two
        self.page['has_related_card_item_three'] = has_related_card_item_three

        return super().get_context_data(*args, **kwargs)
