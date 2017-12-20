from bs4 import BeautifulSoup

from core.templatetags.image_tags import progressive_image


def test_progressive_image(settings):
    settings.STATICFILES_STORAGE = (
        'django.contrib.staticfiles.storage.StaticFilesStorage'
    )

    expected = """
        <picture id="picture">
            <source
                srcset="/static/images/export-hp-export-opportunities.webp"
                type="image/webp"
            >
            <img
                src="/static/images/export-hp-export-opportunities.jpg"
                alt="hello"
            >
        </picture>
    """

    actual = progressive_image(
        webp='images/export-hp-export-opportunities.webp',
        src='images/export-hp-export-opportunities.jpg',
        alt_text='hello',
        img_id='picture'
    )

    assert (
        str(BeautifulSoup(expected, 'html.parser')) ==
        str(BeautifulSoup(actual, 'html.parser'))
    )
