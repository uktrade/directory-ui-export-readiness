import abc

from bs4 import BeautifulSoup
import markdown2

from django.template.loader import render_to_string
from django.utils.functional import cached_property

from api_client import api_client
from article import structure


WORDS_PER_SECOND = 1.5  # Average word per second on screen


def markdown_to_html(markdown_file_path, context={}):
    content = render_to_string(markdown_file_path, context)
    return markdown2.markdown(content, extras=["target-blank-links"])


def get_word_count(html):
    soup = BeautifulSoup(html.replace('\n', ''), 'html.parser')
    words = ''.join(soup.findAll(text=True)).strip()
    return len(words.split(' '))


def time_to_read_in_seconds(article):
    html = markdown_to_html(article.markdown_file_path)
    return round(get_word_count(html) / WORDS_PER_SECOND)


class BaseArticlesViewedManager(abc.ABC):
    def __init__(self, request):
        self.request = request

    def get_view_progress_for_groups(self):
        return {
            group.name: {
                'read': len(self.viewed_article_uuids & group.article_uuids),
                'total': len(group.article_uuids),
            }
            for group in structure.ALL_GROUPS
        }

    def articles_viewed_for_group(self, group_name):
        group = structure.get_article_group(group_name)
        # `&` performs an intersection of items in both sets
        return self.viewed_article_uuids & group.article_uuids

    def remaining_read_time_for_group(self, group_name):
        group = structure.get_article_group(group_name)
        return group.remaining_time_to_read(self.viewed_article_uuids)

    @cached_property
    def viewed_article_uuids(self):
        return self.retrieve_viewed_article_uuids()

    @abc.abstractmethod
    def retrieve_viewed_article_uuids(self):
        return


class ArticlesViewedManagerFactory:
    def __new__(cls, request, current_article=None):
        if request.sso_user is None:
            factory_function = cls.get_session_articles_viewed_manager
        else:
            factory_function = cls.get_database_articles_viewed_manager
        return factory_function(request, current_article)

    @staticmethod
    def get_session_articles_viewed_manager(request, current_article):
        session_manager = SessionArticlesViewedManager(request)
        if current_article:
            session_manager.persist_article(current_article.uuid)
        return session_manager

    @staticmethod
    def get_database_articles_viewed_manager(request, current_article):
        session_manager = SessionArticlesViewedManager(request)
        database_manager = DatabaseArticlesViewedManager(request)

        # write article views stored in the session to the database
        viewed_article_uuids = set()
        if current_article:
            viewed_article_uuids.add(current_article.uuid)
        if session_manager.viewed_article_uuids:
            viewed_article_uuids.update(session_manager.viewed_article_uuids)
        response = database_manager.persist_articles(viewed_article_uuids)
        if response.ok:
            session_manager.clear()
        return database_manager


class SessionArticlesViewedManager(BaseArticlesViewedManager):
    SESSION_KEY = 'ARTICLES_READ'

    def persist_article(self, article_uuid):
        articles = self.request.session.get(self.SESSION_KEY, [])
        articles.append(article_uuid)
        self.request.session[self.SESSION_KEY] = articles
        self.request.session.modified = True

    def retrieve_viewed_article_uuids(self):
        uuids = self.request.session.get(self.SESSION_KEY, [])
        return set(uuids)

    def clear(self):
        self.request.session[self.SESSION_KEY] = []


class DatabaseArticlesViewedManager(BaseArticlesViewedManager):

    article_uuids = set()

    def persist_articles(self, article_uuids):
        response = api_client.exportreadiness.bulk_create_article_read(
            article_uuids=article_uuids,
            sso_session_id=self.request.sso_user.session_id,
        )
        assert response.ok, response.content
        self.article_uuids = set(
            [article['article_uuid'] for article in response.json()]
        )
        return response

    def retrieve_viewed_article_uuids(self):
        # for performance gains (ED-2822) the articles are returned by API when
        # bulk_persist_article was called by ArticleViewedManager
        return self.article_uuids
