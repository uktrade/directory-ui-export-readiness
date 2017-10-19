from bs4 import BeautifulSoup
import markdown2

from django.template.loader import render_to_string


def markdown_to_html(markdown_file_path):
    html = render_to_string(markdown_file_path)
    return markdown2.markdown(html)


def get_article_share_title(markdown_file_path):
    html = markdown_to_html(markdown_file_path)
    soup = BeautifulSoup(html)
    return 'Export Readiness - ' + soup.find('h1').text


def build_social_link(template, request, markdown_file_path):
    return template.format(
        url=request.build_absolute_uri(),
        text=get_article_share_title(markdown_file_path),
    )


def build_twitter_link(request, markdown_file_path):
    template = 'https://twitter.com/intent/tweet?text={text} {url}'
    return build_social_link(template, request, markdown_file_path)


def build_facebook_link(request, markdown_file_path):
    template = 'http://www.facebook.com/share.php?u={url}'
    return build_social_link(template, request, markdown_file_path)


def build_linkedin_link(request, markdown_file_path):
    template = (
        'https://www.linkedin.com/shareArticle'
        '?mini=true&url={url}&title={text}&source=LinkedIn'
    )
    return build_social_link(template, request, markdown_file_path)


def build_email_link(request, markdown_file_path):
    template = 'mailto:?body={text}&subject={url}'
    return build_social_link(template, request, markdown_file_path)
