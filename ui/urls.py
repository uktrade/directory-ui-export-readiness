from django.conf.urls import url
from django.views.generic import TemplateView

import core.views


urlpatterns = [
    url(
        r"^robots\.txt$",
        TemplateView.as_view(
            template_name='robots.txt', content_type='text/plain'
        ),
        name='robots'
    ),
    url(
        r"^$",
        core.views.LandingPagelView.as_view(),
        name='landing-page',
    ),
]
