from directory_constants.constants import cms

from django.views.generic import TemplateView

from prototype.mixins import (
    GetCMSTagMixin,
    SocialLinksMixin,
    BreadcrumbsMixin,
)
from core.mixins import (
    PrototypeFeatureFlagMixin,
    NewsSectionFeatureFlagMixin,
    GetCMSComponentMixin,
    GetCMSPageMixin,
)
from euexit.mixins import HideLanguageSelectorMixin

TEMPLATE_MAPPING = {
    'TopicLandingPage': 'prototype/topic_list.html',
    'SuperregionPage': 'prototype/superregion.html',
    'CountryGuidePage': 'prototype/country_guide.html',
    'ArticleListingPage': 'prototype/article_list.html',
    'ArticlePage': 'prototype/article_detail.html'
}


class PrototypeTemplateChooserMixin:
    @property
    def template_name(self):
        return TEMPLATE_MAPPING[self.page['page_type']]


class PrototypePageView(
    BreadcrumbsMixin,
    PrototypeFeatureFlagMixin,
    PrototypeTemplateChooserMixin,
    GetCMSPageMixin,
    TemplateView,
):
    @property
    def slug(self):
        return self.kwargs['slug']


class TagListPageView(
    PrototypeFeatureFlagMixin,
    GetCMSTagMixin,
    TemplateView,
):
    template_name = 'prototype/tag_list.html'

    @property
    def slug(self):
        return self.kwargs['slug']


class NewsListPageView(
    NewsSectionFeatureFlagMixin,
    GetCMSPageMixin,
    TemplateView,
):
    template_name = 'prototype/domestic_news_list.html'
    slug = cms.EXPORT_READINESS_EU_EXIT_DOMESTIC_NEWS_SLUG


class NewsArticleDetailView(
    SocialLinksMixin,
    NewsSectionFeatureFlagMixin,
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
    component_slug = cms.COMPONENTS_BANNER_DOMESTIC_SLUG
    slug = cms.EXPORT_READINESS_EU_EXIT_INTERNATIONAL_NEWS_SLUG


class InternationalNewsArticleDetailView(NewsArticleDetailView):
    template_name = 'prototype/international_news_detail.html'
