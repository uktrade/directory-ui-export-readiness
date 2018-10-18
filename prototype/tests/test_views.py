from unittest.mock import patch

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
            'landing_page_title': 'Africa',
            'full_path': '/markets/africa/',
            'hero_image': {'url': 'africa.png'},
            'articles_count': 0,
            'last_published_at': '2018-10-01T15:15:53.927833Z'
        },
        {
            'landing_page_title': 'Asia',
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

    assert 'Asia' in str(response.content)
    assert 'Africa' not in str(response.content)
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


@patch('directory_cms_client.client.cms_api_client.lookup_by_full_path')
def test_news_list_page_feature_flag_on(mock_get_page, client, settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'NEWS_SECTION_ON': True,
    }

    news_list_page = {
        'title': 'News CMS admin title',
        'landing_page_title': 'News',
        'article_listing': [
            {
                'landing_page_title': 'Lorem ipsum',
                'full_path': '/news/lorem-ipsum/',
                'hero_image': {'url': 'lorem_ipsum.png'},
                'articles_count': 0,
                'last_published_at': '2018-10-01T15:15:53.927833Z'
            },
            {
                'landing_page_title': 'Dolor sit amet',
                'full_path': '/news/dolor-sit-amet/',
                'hero_image': {'url': 'dolor_sit_amet.png'},
                'articles_count': 3,
                'last_published_at': '2018-10-01T15:16:30.583279Z'
            }
        ],
    }

    url = reverse('news-article-list')

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=news_list_page
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['prototype/domestic_news_list.html']

    assert news_list_page['title'] not in str(response.content)
    assert news_list_page['landing_page_title'] in str(response.content)


def test_news_list_page_feature_flag_off(client, settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'NEWS_SECTION_ON': False,
    }

    url = reverse('news-article-list')

    response = client.get(url)

    assert response.status_code == 404
