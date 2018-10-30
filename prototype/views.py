from django.views.generic import TemplateView
from prototype.mixins import (
    GetCMSPageByFullPathMixin,
    GetCMSTagMixin,
    SocialLinksMixin,
    RelatedContentMixin,
)
from core.mixins import (
    PrototypeFeatureFlagMixin,
    NewsSectionFeatureFlagMixin,
    GetCMSComponentMixin,
    GetCMSPageMixin,
)
from euexit.mixins import HideLanguageSelectorMixin


class TopicListPageView(
    PrototypeFeatureFlagMixin,
    GetCMSPageByFullPathMixin,
    TemplateView,
):
    template_name = 'prototype/topic_list.html'


class ArticleListPageView(
    PrototypeFeatureFlagMixin,
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
    GetCMSPageByFullPathMixin,
    TemplateView,
):
    template_name = 'prototype/article_detail.html'


class NewsListPageView(
    NewsSectionFeatureFlagMixin,
    GetCMSPageMixin,
    TemplateView,
):
    template_name = 'prototype/domestic_news_list.html'
    slug = 'eu-exit-news'


class NewsArticleDetailView(
    SocialLinksMixin,
    NewsSectionFeatureFlagMixin,
    RelatedContentMixin,
    GetCMSPageMixin,
    TemplateView,
):
    template_name = 'prototype/domestic_news_detail.html'

    @property
    def slug(self):
        return self.kwargs['slug']


class InternationalNewsListPageView(
    NewsSectionFeatureFlagMixin,
    GetCMSPageMixin,
    GetCMSComponentMixin,
    HideLanguageSelectorMixin,
    TemplateView,
):
    template_name = 'prototype/international_news_list.html'
    component_slug = 'eu-exit-banner-domestic'
    slug = 'international-eu-exit-news'


class InternationalNewsArticleDetailView(NewsArticleDetailView):
    template_name = 'prototype/international_news_detail.html'
