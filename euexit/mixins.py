from core.mixins import TranslationsMixin, NotFoundOnDisabledFeature
from django.conf import settings


class EUExitFormsFeatureFlagMixin(NotFoundOnDisabledFeature):
    @property
    def flag(self):
        return settings.FEATURE_FLAGS['EU_EXIT_FORMS_ON']


class HideLanguageSelectorMixin(TranslationsMixin):
    def get_context_data(self, **kwargs):
        return super().get_context_data(
            hide_language_selector=True,
            **kwargs,
        )
