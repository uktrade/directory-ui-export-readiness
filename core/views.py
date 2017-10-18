from django.views.generic import TemplateView


class LandingPagelView(TemplateView):
    template_name = 'core/landing-page.html'
