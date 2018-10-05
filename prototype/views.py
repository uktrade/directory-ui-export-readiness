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
