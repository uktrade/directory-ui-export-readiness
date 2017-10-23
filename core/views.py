from django.views.generic import TemplateView
from triage.helpers import TriageAnswersManager

from casestudy import casestudies

class LandingPagelView(TemplateView):
    template_name = 'core/landing-page.html'

    def get_context_data(self, *args, **kwargs):
        answer_manager = TriageAnswersManager(self.request)
        has_completed_triage = answer_manager.retrieve_answers() != {}
        return super().get_context_data(
            *args, **kwargs,
            has_completed_triage=has_completed_triage,
            casestudies=[
                casestudies.MARKETPLACE,
                casestudies.HELLO_BABY,
                casestudies.YORK,
            ],
        )
