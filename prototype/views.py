from prototype.mixins import (
    GetCMSPageByFullPathMixin,
    SocialLinksMixin,
    InternationalNewsCMSLookupPath,
    PrototypeCMSLookupPath,
    RelatedContentMixin,
)
from core.mixins import PrototypeFeatureFlagMixin, NewsSectionFeatureFlagMixin


class TopicListPageView(
    PrototypeFeatureFlagMixin,
    PrototypeCMSLookupPath,  # must come before GetCMSPageByFullPathMixin
    GetCMSPageByFullPathMixin,
):
    template_name = 'prototype/topic_list.html'


class ArticleListPageView(
    PrototypeFeatureFlagMixin,
    PrototypeCMSLookupPath,
    GetCMSPageByFullPathMixin,
):
    template_name = 'prototype/article_list.html'


class ArticleDetailView(
    SocialLinksMixin,
    PrototypeFeatureFlagMixin,
    RelatedContentMixin,
    PrototypeCMSLookupPath,
    GetCMSPageByFullPathMixin,
):
    template_name = 'prototype/article_detail.html'


class NewsListPageView(
    NewsSectionFeatureFlagMixin,
    GetCMSPageByFullPathMixin,
):
    template_name = 'prototype/domestic_news_list.html'


class NewsArticleDetailView(
    SocialLinksMixin,
    NewsSectionFeatureFlagMixin,
    RelatedContentMixin,
    PrototypeCMSLookupPath,
    GetCMSPageByFullPathMixin,
):
    template_name = 'prototype/domestic_news_detail.html'


class InternationalNewsListPageView(
    NewsSectionFeatureFlagMixin,
    InternationalNewsCMSLookupPath,
    GetCMSPageByFullPathMixin,
):
    template_name = 'prototype/international_news_list.html'


class InternationalNewsArticleDetailView(
    SocialLinksMixin,
    NewsSectionFeatureFlagMixin,
    RelatedContentMixin,
    InternationalNewsCMSLookupPath,
    GetCMSPageByFullPathMixin,
):
    template_name = 'prototype/international_news_detail.html'
