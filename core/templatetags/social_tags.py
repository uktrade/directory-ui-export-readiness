from django import template
import urllib.parse

register = template.Library()


@register.simple_tag
def build_twitter_link(text, url):
    encoded_text = urllib.parse.quote(text + ' ')
    link = 'https://twitter.com/intent/tweet?text={}{}'
    return link.format(encoded_text, url)


@register.simple_tag
def build_facebook_link(url):
    return 'https://www.facebook.com/share.php?u={}'.format(url)


@register.simple_tag
def build_linkedin_link(text, url):
    encoded_text = urllib.parse.quote(text)
    link = (
        'https://www.linkedin.com/shareArticle'
        '?mini=true&url={}&title={}&source=LinkedIn'
    ).format(url, encoded_text)
    return link


@register.simple_tag
def build_email_link(text, url):
    encoded_text = urllib.parse.quote(text)
    return 'mailto:?body={}&subject={}'.format(url, encoded_text)
