from django.views.generic import TemplateView
from prototype.mixins import (
    GetCMSPageByFullPathMixin,
    GetCMSTagMixin,
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
    TemplateView,
):
    template_name = 'prototype/topic_list.html'


class ArticleListPageView(
    PrototypeFeatureFlagMixin,
    PrototypeCMSLookupPath,
    GetCMSPageByFullPathMixin,
    TemplateView,
):
    template_name = 'prototype/article_list.html'


class TagListPageView(
    PrototypeFeatureFlagMixin,
    GetCMSTagMixin,
    TemplateView,
):
    template_name = 'prototype/tag_list.html'

    @property
    def slug(self):
        return self.kwargs['slug']


class ArticleDetailView(
    SocialLinksMixin,
    PrototypeFeatureFlagMixin,
    RelatedContentMixin,
    PrototypeCMSLookupPath,
    GetCMSPageByFullPathMixin,
    TemplateView,
):
    template_name = 'prototype/article_detail.html'


class NewsListPageView(
    NewsSectionFeatureFlagMixin,
    GetCMSPageByFullPathMixin,
    TemplateView,
):
    template_name = 'prototype/domestic_news_list.html'


class NewsArticleDetailView(
    SocialLinksMixin,
    NewsSectionFeatureFlagMixin,
    RelatedContentMixin,
    PrototypeCMSLookupPath,
    GetCMSPageByFullPathMixin,
    TemplateView,
):
    template_name = 'prototype/domestic_news_detail.html'


class InternationalNewsListPageView(
    NewsSectionFeatureFlagMixin,
    InternationalNewsCMSLookupPath,
    GetCMSPageByFullPathMixin,
    TemplateView,
):
    template_name = 'prototype/international_news_list.html'


class InternationalNewsArticleDetailView(
    SocialLinksMixin,
    NewsSectionFeatureFlagMixin,
    RelatedContentMixin,
    InternationalNewsCMSLookupPath,
    GetCMSPageByFullPathMixin,
    TemplateView,
):
    template_name = 'prototype/international_news_detail.html'
