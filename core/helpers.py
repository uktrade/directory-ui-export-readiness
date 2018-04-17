import urllib.parse
from directory_cms_client import DirectoryCMSClient
from django.conf import settings


cms_client = DirectoryCMSClient(
    base_url=settings.CMS_URL,
    api_key=settings.CMS_SIGNATURE_SECRET,
)


def build_social_link(template, request, title):
    text_to_encode = 'Export Readiness - ' + title + ' '
    return template.format(
        url=request.build_absolute_uri(),
        text=urllib.parse.quote(text_to_encode)
    )


def build_twitter_link(request, title):
    template = 'https://twitter.com/intent/tweet?text={text}{url}'
    return build_social_link(template, request, title)


def build_facebook_link(request, title):
    template = 'https://www.facebook.com/share.php?u={url}'
    return build_social_link(template, request, title)


def build_linkedin_link(request, title):
    template = (
        'https://www.linkedin.com/shareArticle'
        '?mini=true&url={url}&title={text}&source=LinkedIn'
    )
    return build_social_link(template, request, title)


def build_email_link(request, title):
    template = 'mailto:?body={url}&subject={text}'
    return build_social_link(template, request, title)


def build_social_links(request, title):
    kwargs = {'request': request, 'title': title}
    return {
        'facebook': build_facebook_link(**kwargs),
        'twitter': build_twitter_link(**kwargs),
        'linkedin': build_linkedin_link(**kwargs),
        'email': build_email_link(**kwargs),
    }
