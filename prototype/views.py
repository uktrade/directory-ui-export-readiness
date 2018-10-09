from directory_components.helpers import SocialLinkBuilder

from prototype.mixins import GetCMSPageByFullPathMixin, SlugFromKwargsMixin
from core.mixins import PrototypeFeatureFlagMixin, NewsSectionFeatureFlagMixin


class NewsListPageView(NewsSectionFeatureFlagMixin, GetCMSPageByFullPathMixin):
    template_name = 'prototype/news_list.html'


class TopicListPageView(
    PrototypeFeatureFlagMixin, GetCMSPageByFullPathMixin, SlugFromKwargsMixin
):
    template_name = 'prototype/topic_list.html'


class ArticleListPageView(
    PrototypeFeatureFlagMixin, GetCMSPageByFullPathMixin, SlugFromKwargsMixin
):
    template_name = 'prototype/article_list.html'


class ArticleDetailView(
    PrototypeFeatureFlagMixin, GetCMSPageByFullPathMixin, SlugFromKwargsMixin
):
    template_name = 'prototype/article_detail.html'
    url_name = 'article-detail'

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

        social_links_builder = SocialLinkBuilder(
            self.request.build_absolute_uri(),
            self.page['title'],
            'Great.gov.uk')

        return super().get_context_data(
            social_links=social_links_builder.links,
            *args,
            **kwargs
        )


class NewsArticleDetailView(NewsSectionFeatureFlagMixin, ArticleDetailView):
    template_name = 'prototype/news_detail.html'
    url_name = 'news-article-detail'
