import abc
import markdown2
from bs4 import BeautifulSoup

from django.template.loader import render_to_string

from api_client import api_client

from . import structure


WORDS_PER_MINUTE = 180  # Average WPM on screen


def markdown_to_html(markdown_file_path):
    html = render_to_string(markdown_file_path)
    return markdown2.markdown(html)


def filter_lines(lines_list):
    """BeautifulSoup returns \n as lines as well, we filter them out.

    It's a function because more filtering can be added later.
    """
    return filter(lambda x: x != '\n', lines_list)


def lines_list_from_html(html):
    """Parses the HTML to return text lines."""
    soup = BeautifulSoup(html, 'html.parser')
    return soup.findAll(text=True)


def count_average_word_number_in_lines_list(lines_list, word_length=5):
    """Assume average word length, counts how many words in all the lines."""
    total_words = 0
    for line in lines_list:
        total_words += len(line)/word_length
    return total_words


def time_to_read_in_minutes(article):
    """Return rounded time to read in minutes give an Article object."""
    html = markdown_to_html(article.markdown_file_path)
    lines_list = lines_list_from_html(html)
    filtered_lines_list = filter_lines(lines_list)
    total_words_count = count_average_word_number_in_lines_list(
        filtered_lines_list
    )
    return round(total_words_count / WORDS_PER_MINUTE)


class BaseArticleReadManager(abc.ABC):
    def __init__(self, request):
        self.request = request

    persist_article = abc.abstractproperty()
    retrieve_articles = abc.abstractproperty()

    def article_read_count(self, group_key):
        read_articles = frozenset(self.retrieve_articles())
        articles_in_group = structure.ALL_GROUPS_DICT[group_key].articles_set
        # read_articles_in_category is a new set (intersection)
        # with elements common to read_articles and articles_in_category
        read_articles_in_group = read_articles & articles_in_group
        return len(read_articles_in_group)

    def remaining_reading_time_in_group(self, group_key):
        pass


class ArticleReadManager:
    def __new__(cls, request):
        if request.sso_user is None:
            return SessionArticlesReadManager(request)
        return DatabaseArticlesReadManager(request)


class SessionArticlesReadManager(BaseArticleReadManager):
    SESSION_KEY = 'ARTICLES_READ'

    def __init__(self, request):
        super().__init__(request)
        self.session = request.session

    def persist_article(self, article_uuid):
        articles = self.session.get(self.SESSION_KEY, [])
        articles.append(article_uuid)
        self.session[self.SESSION_KEY] = articles
        self.session.modified = True

    def retrieve_articles(self):
        return self.request.session.get(self.SESSION_KEY, [])


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
