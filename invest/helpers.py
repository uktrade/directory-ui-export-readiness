from django.conf import settings

from directory_cms_client.client import DirectoryCMSClient

cms_api_client = DirectoryCMSClient(
    base_url=settings.DIRECTORY_CMS_API_CLIENT_BASE_URL,
    api_key=settings.DIRECTORY_CMS_API_CLIENT_API_KEY,
    sender_id=settings.DIRECTORY_CMS_API_CLIENT_SENDER_ID,
    timeout=settings.DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT,
    service_name='INVEST',
)
