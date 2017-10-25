import abc

import markdown2

from django.template.loader import render_to_string

from api_client import api_client

from . import structure


def markdown_to_html(markdown_file_path):
    html = render_to_string(markdown_file_path)
    return markdown2.markdown(html)


class BaseArticleReadManager(abc.ABC):
    def __init__(self, request):
        self.request = request

    persist_article = abc.abstractproperty()
    retrieve_articles = abc.abstractproperty()
    article_read_count = abc.abstractproperty()


class ArticleReadManager:
    def __new__(cls, request):
        if request.sso_user is None:
            return SessionArticlesReadManager(request)
        return DatabaseArticlesReadManager(request)


class SessionArticlesReadManager(BaseArticleReadManager):
    SESSION_KEY = 'ARTICLES_READ'

    def persist_article(self, article_uuid):
        session = self.request.session
        articles = session.get(self.SESSION_KEY, [])
        articles.append(article_uuid)
        session[self.SESSION_KEY] = articles
        session.modified = True

    def retrieve_articles(self):
        return self.request.session.get(self.SESSION_KEY, [])

    def article_read_count(self, category):
        if category not in structure.CATEGORIES_LOOKUP:
            raise Exception('Incorrect category')

        session = self.request.session
        read_articles = frozenset(session.get(self.SESSION_KEY, []))
        articles_in_category = frozenset(
            [article.uuid for article in
             structure.CATEGORIES_LOOKUP[category].articles]
        )
        read_articles_in_category = read_articles & articles_in_category
        return len(read_articles_in_category)


class DatabaseArticlesReadManager(BaseArticleReadManager):

    def persist_article(self, article_uuid):
        response = api_client.exportreadiness.create_article_read(
            article_uuid=article_uuid,
            sso_session_id=self.request.sso_user.session_id,
        )
        response.raise_for_status()

    def retrieve_articles(self):
        response = api_client.exportreadiness.retrieve_article_read(
            sso_session_id=self.request.sso_user.session_id
        )
        response.raise_for_status()
        return [article['article_uuid'] for article in response.json()]

    def article_read_count(self, category):
        if category not in structure.CATEGORIES_LOOKUP:
            raise Exception('Incorrect category')

        read_articles = frozenset(self.retrieve_articles())
        articles_in_category = frozenset(
            [article.uuid for article in
             structure.CATEGORIES_LOOKUP[category].articles]
        )
        read_articles_in_category = read_articles & articles_in_category
        return len(read_articles_in_category)
