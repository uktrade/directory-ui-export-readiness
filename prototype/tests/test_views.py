from unittest.mock import patch, PropertyMock
from bs4 import BeautifulSoup
from django.urls import reverse

from core.tests.helpers import create_response


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_prototype_landing_page_news_section(mock_get_page, client, settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'NEWS_SECTION_ON': True,
    }

    url = reverse('prototype-landing-page')

    page = {
        'news_title': 'News',
        'news_description': '<p>Lorem ipsum</p>',
        'articles': [
            {'article_title': 'News article 1'},
            {'article_title': 'News article 2'},
        ],
    }

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=page
    )
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['prototype/landing_page.html']

    assert page['news_title'] in str(response.content)
    assert '<p class="body-text">Lorem ipsum</p>' in str(response.content)
    assert 'News article 1' in str(response.content)
    assert 'News article 2' in str(response.content)


test_topic_page = {
    'title': 'Markets CMS admin title',
    'landing_page_title': 'Markets',
    'hero_image': {'url': 'markets.png'},
    'article_listing': [
        {
            'landing_page_title': 'Africa market information',
            'full_path': '/markets/africa/',
            'hero_image': {'url': 'africa.png'},
            'articles_count': 0,
            'last_published_at': '2018-10-01T15:15:53.927833Z'
        },
        {
            'landing_page_title': 'Asia market information',
            'full_path': '/markets/asia/',
            'hero_image': {'url': 'asia.png'},
            'articles_count': 3,
            'last_published_at': '2018-10-01T15:16:30.583279Z'
        }
    ],
}


@patch('directory_cms_client.client.cms_api_client.lookup_by_full_path')
def test_prototype_topic_list_page(mock_get_page, client, settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'PROTOTYPE_PAGES_ON': True,
        'PROTOTYPE_HEADER_FOOTER_ON': False,
    }

    url = reverse('topic-list', kwargs={'slug': 'markets'})

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=test_topic_page
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['prototype/topic_list.html']

    assert test_topic_page['title'] not in str(response.content)
    assert test_topic_page['landing_page_title'] in str(response.content)

    assert 'Asia market information' in str(response.content)
    assert 'Africa market information' not in str(response.content)
    assert 'markets.png' in str(response.content)
    assert 'asia.png' in str(response.content)
    assert 'africa.png' not in str(response.content)
    assert '01 October 2018' in str(response.content)


@patch('directory_cms_client.client.cms_api_client.lookup_by_full_path')
def test_prototype_article_detail_page_no_related_content(
    mock_get_page, client, settings
):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'PROTOTYPE_PAGES_ON': True,
    }

    test_article_page_no_related_content = {
        "title": "Test article admin title",
        "article_title": "Test article",
        "article_teaser": "Test teaser",
        "article_image": {"url": "foobar.png"},
        "article_body_text": "<p>Lorem ipsum</p>",
        "related_article_one_url": "",
        "related_article_one_title": "",
        "related_article_one_teaser": "",
        "related_article_two_url": "",
        "related_article_two_title": "",
        "related_article_two_teaser": "",
        "related_article_three_url": "",
        "related_article_three_title": "",
        "related_article_three_teaser": "",
        "full_path": "/markets/foo/bar/",
        "last_published_at": "2018-10-09T16:25:13.142357Z",
        "meta": {
            "slug": "bar",
        },
    }

    url = reverse('article-detail', kwargs={
        'topic': 'markets',
        'list': 'foo',
        'slug': 'bar',
    })

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=test_article_page_no_related_content
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['prototype/article_detail.html']

    assert 'Related content' not in str(response.content)


@patch('directory_cms_client.client.cms_api_client.lookup_by_full_path')
def test_prototype_article_detail_page_one_related_content(
    mock_get_page, client, settings
):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'PROTOTYPE_PAGES_ON': True,
    }

    article_page = {
        "title": "Test article admin title",
        "article_title": "Test article",
        "article_teaser": "Test teaser",
        "article_image": {"url": "foobar.png"},
        "article_body_text": "<p>Lorem ipsum</p>",
        "related_article_one_url": "#",
        "related_article_one_title": "Foo",
        "related_article_one_teaser": "Bar",
        "related_article_two_url": "",
        "related_article_two_title": "",
        "related_article_two_teaser": "",
        "related_article_three_url": "",
        "related_article_three_title": "",
        "related_article_three_teaser": "",
        "full_path": "/markets/foo/bar/",
        "last_published_at": "2018-10-09T16:25:13.142357Z",
        "meta": {
            "slug": "bar",
        },
    }

    url = reverse('article-detail', kwargs={
        'topic': 'markets',
        'list': 'foo',
        'slug': 'bar',
    })

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=article_page
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['prototype/article_detail.html']

    assert 'Related content' in str(response.content)
    assert '<a href="#" class="link">Foo</a>' in str(response.content)


@patch('directory_cms_client.client.cms_api_client.lookup_by_full_path')
def test_prototype_article_detail_page_two_related_content(
    mock_get_page, client, settings
):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'PROTOTYPE_PAGES_ON': True,
    }

    article_page = {
        "title": "Test article admin title",
        "article_title": "Test article",
        "article_teaser": "Test teaser",
        "article_image": {"url": "foobar.png"},
        "article_body_text": "<p>Lorem ipsum</p>",
        "related_article_one_url": "",
        "related_article_one_title": "",
        "related_article_one_teaser": "",
        "related_article_two_url": "#2",
        "related_article_two_title": "Foo 2",
        "related_article_two_teaser": "Bar 2",
        "related_article_three_url": "#3",
        "related_article_three_title": "Foo 3",
        "related_article_three_teaser": "Bar 3",
        "full_path": "/markets/foo/bar/",
        "last_published_at": "2018-10-09T16:25:13.142357Z",
        "meta": {
            "slug": "bar",
        },
    }

    url = reverse('article-detail', kwargs={
        'topic': 'markets',
        'list': 'foo',
        'slug': 'bar',
    })

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=article_page
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['prototype/article_detail.html']

    assert 'Related content' in str(response.content)
    assert '<a href="#2" class="link">Foo 2</a>' in str(response.content)
    assert '<a href="#3" class="link">Foo 3</a>' in str(response.content)


test_news_list_page = {
    'title': 'News CMS admin title',
    'landing_page_title': 'News',
    'articles_count': 2,
    'articles': [
        {
            'article_title': 'Lorem ipsum',
            'full_path': '/eu-exit-news/lorem-ipsum/',
            'last_published_at': '2018-10-01T15:15:53.927833Z',
            'meta': {'slug': 'test-slug-one'},
        },
        {
            'article_title': 'Dolor sit amet',
            'full_path': '/eu-exit-news/dolor-sit-amet/',
            'last_published_at': '2018-10-01T15:16:30.583279Z',
            'meta': {'slug': 'test-slug-two'},
        }
    ],
}


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_news_list_page_feature_flag_on(mock_get_page, client, settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'NEWS_SECTION_ON': True,
    }

    url = reverse('news-article-list')

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=test_news_list_page
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['prototype/domestic_news_list.html']

    assert test_news_list_page['title'] not in str(response.content)
    assert test_news_list_page['landing_page_title'] in str(response.content)
    assert 'Lorem ipsum' in str(response.content)
    assert 'Dolor sit amet' in str(response.content)


@patch('prototype.views.InternationalNewsListPageView.cms_component',
       new_callable=PropertyMock)
@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_international_news_list_page(
    mock_get_page, mock_get_component, client, settings
):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'NEWS_SECTION_ON': True,
    }

    url = reverse('international-news-article-list')

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=test_news_list_page
    )
    mock_get_component.return_value = {
        'banner_label': 'EU Exit updates',
        'banner_content': '<p>Lorem ipsum.</p>',
        'meta': {'languages': ['en-gb', 'English']},
    }

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['prototype/international_news_list.html']

    assert test_news_list_page['title'] not in str(response.content)
    assert test_news_list_page['landing_page_title'] in str(response.content)
    assert 'Lorem ipsum' in str(response.content)
    assert 'Dolor sit amet' in str(response.content)


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_domestic_news_article_detail_page(mock_get_page, client, settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'NEWS_SECTION_ON': True,
    }

    test_article_page = {
        "title": "Test article admin title",
        "article_title": "Test news title",
        "article_teaser": "Test news teaser",
        "article_image": {"url": "foobar.png"},
        "article_body_text": "<p>Lorem ipsum</p>",
        "related_article_one_url": "",
        "related_article_one_title": "",
        "related_article_one_teaser": "",
        "related_article_two_url": "",
        "related_article_two_title": "",
        "related_article_two_teaser": "",
        "related_article_three_url": "",
        "related_article_three_title": "",
        "related_article_three_teaser": "",
        "full_path": "/markets/foo/bar/",
        "last_published_at": "2018-10-09T16:25:13.142357Z",
        "meta": {
            "slug": "foo",
        },
    }

    url = reverse('news-article-detail', kwargs={'slug': 'foo'})

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=test_article_page
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [
        'prototype/domestic_news_detail.html']

    assert 'Test news title' in str(response.content)
    assert 'Test news teaser' in str(response.content)
    assert '<p class="body-text">Lorem ipsum</p>' in str(response.content)


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_international_news_article_detail_page(
    mock_get_page, client, settings
):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'NEWS_SECTION_ON': True,
    }

    test_article_page = {
        "title": "Test article admin title",
        "article_title": "Test news title",
        "article_teaser": "Test news teaser",
        "article_image": {"url": "foobar.png"},
        "article_body_text": "<p>Lorem ipsum</p>",
        "related_article_one_url": "",
        "related_article_one_title": "",
        "related_article_one_teaser": "",
        "related_article_two_url": "",
        "related_article_two_title": "",
        "related_article_two_teaser": "",
        "related_article_three_url": "",
        "related_article_three_title": "",
        "related_article_three_teaser": "",
        "full_path": "/markets/foo/bar/",
        "last_published_at": "2018-10-09T16:25:13.142357Z",
        "meta": {
            "slug": "foo",
        },
    }

    url = reverse('international-news-article-detail', kwargs={'slug': 'foo'})

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=test_article_page
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [
        'prototype/international_news_detail.html']

    assert 'Test news title' in str(response.content)
    assert 'Test news teaser' in str(response.content)
    assert '<p class="body-text">Lorem ipsum</p>' in str(response.content)


def test_news_list_page_feature_flag_off(client, settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'NEWS_SECTION_ON': False,
    }

    url = reverse('news-article-list')

    response = client.get(url)

    assert response.status_code == 404


test_articles = [
    {
        'seo_title': 'SEO title article 1',
        'search_description': 'Search description article 1',
        'article_title': 'Article 1 title',
        'article_teaser': 'Article 1 teaser.',
        'article_image': {'url': 'article_image1.png'},
        'article_body_text': '<p>Lorem ipsum 1</p>',
        'last_published_at': '2018-10-01T15:16:30.583279Z',
        'full_path': '/topic/list/article-one/',
        'tags': [
            {'name': 'New to exporting', 'slug': 'new-to-exporting'},
            {'name': 'Export tips', 'slug': 'export-tips'}
        ],
        'meta': {'slug': 'article-one'}
    },
    {
        'seo_title': 'SEO title article 2',
        'search_description': 'Search description article 2',
        'article_title': 'Article 2 title',
        'article_teaser': 'Article 2 teaser.',
        'article_image': {'url': 'article_image2.png'},
        'article_body_text': '<p>Lorem ipsum 2</p>',
        'last_published_at': '2018-10-02T15:16:30.583279Z',
        'full_path': '/topic/list/article-two/',
        'tags': [
            {'name': 'New to exporting', 'slug': 'new-to-exporting'},
        ],
        'meta': {'slug': 'article-two'}
    },
]

test_list_page = {
    'title': 'List CMS admin title',
    'seo_title': 'SEO title article list',
    'search_description': 'Article list search description',
    'landing_page_title': 'Article list landing page title',
    'hero_image': {'url': 'article_list.png'},
    'hero_teaser': 'Article list hero teaser',
    'list_teaser': '<p>Article list teaser</p>',
    'articles': test_articles,
}


@patch('directory_cms_client.client.cms_api_client.lookup_by_full_path')
def test_prototype_article_list_page(mock_get_page, client, settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'PROTOTYPE_PAGES_ON': True,
    }

    url = reverse('article-list', kwargs={
        'topic': 'topic',
        'slug': 'list',
    })

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=test_list_page
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['prototype/article_list.html']

    assert test_list_page['title'] not in str(response.content)
    assert test_list_page['landing_page_title'] in str(response.content)

    assert '01 October' in str(response.content)
    assert '02 October' in str(response.content)


test_tag_page = {
    'meta': {'total_count': 2},
    'items': test_articles,
}


@patch('directory_cms_client.client.cms_api_client.lookup_by_tag')
def test_prototype_tag_list_page(mock_get_page, client, settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'PROTOTYPE_PAGES_ON': True,
    }

    url = reverse('tag-list', kwargs={'slug': 'new-to-exporting'})

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=test_tag_page
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['prototype/tag_list.html']

    assert '01 October' in str(response.content)
    assert '02 October' in str(response.content)
    assert 'Article 1 title' in str(response.content)
    assert 'Article 2 title' in str(response.content)
    assert 'Articles with tag: new-to-exporting' in str(response.content)
    assert '2 articles' in str(response.content)


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_prototype_landing_page_header_footer_default_links(
    mock_get_page, client, settings
):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'PROTOTYPE_PAGES_ON': True,
        'PROTOTYPE_HEADER_FOOTER_ON': True,
    }

    url = reverse('prototype-landing-page')

    page = {
        'news_title': 'News',
        'news_description': '<p>Lorem ipsum</p>',
        'articles': [],
    }

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=page
    )
    response = client.get(url)

    assert response.status_code == 200

    soup = BeautifulSoup(response.content, 'html.parser')

    assert soup.find(id="header-markets-link")
    assert soup.find(id="header-industries-link")
    assert soup.find(id="header-services-link")
    assert soup.find(id="header-about-link")

    home_link = soup.find(id="header-dit-logo")
    assert home_link['href'] == 'https://invis.io/GROOBO8PYQV'

    header_advice_link = soup.find(id="header-advice-link")
    assert header_advice_link['href'] == '/prototype/advice-and-guidance/'

    footer_advice_link = soup.find(id="footer-advice-link")
    assert footer_advice_link['href'] == '/prototype/advice-and-guidance/'


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_prototype_landing_page_header_footer(mock_get_page, client, settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'PROTOTYPE_PAGES_ON': True,
        'PROTOTYPE_HEADER_FOOTER_ON': True,
    }

    settings.PROTOTYPE_HOME_LINK = '/foo'
    settings.PROTOTYPE_ADVICE_LINK = '/advice'

    url = reverse('prototype-landing-page')

    page = {
        'news_title': 'News',
        'news_description': '<p>Lorem ipsum</p>',
        'articles': [],
    }

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=page
    )
    response = client.get(url)

    assert response.status_code == 200

    soup = BeautifulSoup(response.content, 'html.parser')

    home_link = soup.find(id="header-dit-logo")
    assert home_link['href'] == '/foo'

    header_advice_link = soup.find(id="header-advice-link")
    assert header_advice_link['href'] == '/advice'

    footer_advice_link = soup.find(id="footer-advice-link")
    assert footer_advice_link['href'] == '/advice'
