from django.views.generic import TemplateView

from core.helpers import build_social_links


class BaseCaseStudyView(TemplateView):
    def get_context_data(self, *args, **kwargs):
        social_links = build_social_links(
            request=self.request, title=self.title
        )
        return super().get_context_data(
            *args, **kwargs,
            social_links=social_links,
            title=self.title,
        )


class CasestudyHelloBabyView(BaseCaseStudyView):
    template_name = 'casestudy/hello-baby.html'
    title = "Hello Baby's rapid online growth"


class CasestudyMarketplaceView(BaseCaseStudyView):
    template_name = 'casestudy/marketplace.html'
    title = "Online marketplaces propel FreestyleXtreme"


class CasestudyYorkBagView(BaseCaseStudyView):
    template_name = 'casestudy/york-bag.html'
    title = "York bag retailer goes global via e-commerce"
