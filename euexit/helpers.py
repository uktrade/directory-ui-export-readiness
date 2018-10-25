from django.conf import settings

from directory_forms_api_client.client import APIFormsClient


eu_exit_forms_api_client = APIFormsClient(
    base_url=settings.DIRECTORY_FORMS_API_BASE_URL,
    api_key=settings.DIRECTORY_FORMS_API_API_KEY_EUEXIT,
    sender_id=settings.DIRECTORY_FORMS_API_SENDER_ID_EUEXIT,
    timeout=settings.DIRECTORY_FORMS_API_DEFAULT_TIMEOUT,
)
