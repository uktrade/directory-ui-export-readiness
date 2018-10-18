from prototype.mixins import (
    GetCMSPageByFullPathMixin,
    SlugFromKwargsMixin,
    InternationalNewsCMSPageMixin,
    SocialLinksMixin,
)
from core.mixins import PrototypeFeatureFlagMixin, NewsSectionFeatureFlagMixin


class NewsListPageView(NewsSectionFeatureFlagMixin, GetCMSPageByFullPathMixin):
    template_name = 'prototype/domestic_news_list.html'


class InternationalNewsListPageView(
    NewsSectionFeatureFlagMixin, InternationalNewsCMSPageMixin
):
    template_name = 'prototype/international_news_list.html'


class TopicListPageView(
    PrototypeFeatureFlagMixin, GetCMSPageByFullPathMixin, SlugFromKwargsMixin
):
    template_name = 'prototype/topic_list.html'


class ArticleListPageView(
    PrototypeFeatureFlagMixin, GetCMSPageByFullPathMixin, SlugFromKwargsMixin
):
    template_name = 'prototype/article_list.html'


class ArticleDetailView(
    PrototypeFeatureFlagMixin,
    GetCMSPageByFullPathMixin,
    SlugFromKwargsMixin,
    SocialLinksMixin,
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

        return super().get_context_data(
            social_links=self.social_links,
            *args,
            **kwargs)


class NewsArticleDetailView(
    NewsSectionFeatureFlagMixin,
    ArticleDetailView,
):
    template_name = 'prototype/domestic_news_detail.html'
    url_name = 'news-article-detail'


class InternationalNewsArticleDetailView(
    NewsArticleDetailView, InternationalNewsCMSPageMixin,
):
    template_name = 'prototype/international_news_detail.html'
    url_name = 'international-news-article-detail'
