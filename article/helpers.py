import abc

import markdown2

from django.template.loader import render_to_string

from api_client import api_client


def markdown_to_html(markdown_file_path):
    html = render_to_string(markdown_file_path)
    return markdown2.markdown(html)


def build_social_link(template, request, title):
    return template.format(
        url=request.build_absolute_uri(),
        text='Export Readiness - ' + title,
    )


def build_twitter_link(request, title):
    template = 'https://twitter.com/intent/tweet?text={text} {url}'
    return build_social_link(template, request, title)


def build_facebook_link(request, title):
    template = 'http://www.facebook.com/share.php?u={url}'
    return build_social_link(template, request, title)


def build_linkedin_link(request, title):
    template = (
        'https://www.linkedin.com/shareArticle'
        '?mini=true&url={url}&title={text}&source=LinkedIn'
    )
    return build_social_link(template, request, title)


def build_email_link(request, title):
    template = 'mailto:?body={text}&subject={url}'
    return build_social_link(template, request, title)


class BaseArticleReadManager(abc.ABC):
    def __init__(self, request):
        self.request = request

    persist_article = abc.abstractproperty()
    retrieve_articles = abc.abstractproperty()


class ArticleReadManager:
    def __new__(cls, request):
        if request.sso_user is None:
            return SessionArticlesReadManager(request)
        return DatabaseArticlesReadManager(request)


class SessionArticlesReadManager(BaseArticleReadManager):
    SESSION_KEY = 'ARTICLES_READ'

    def persist_article(self, article):
        session = self.request.session
        articles = session.get(self.SESSION_KEY, [])
        articles.append(article)
        session[self.SESSION_KEY] = articles
        session.modified = True

    def retrieve_articles(self):
        return self.request.session.get(self.SESSION_KEY, [])


class DatabaseArticlesReadManager(BaseArticleReadManager):

    def persist_article(self, article):
        response = api_client.exportreadiness.create_article_read(
            form_data=article,
            sso_session_id=self.request.sso_user.session_id,
        )
        response.raise_for_status()

    def retrieve_articles(self):
        response = api_client.exportreadiness.retrieve_article_read(
            sso_session_id=self.request.sso_user.session_id
        )
        response.raise_for_status()
        return response.json()
