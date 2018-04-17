import requests
from directory_cms_client import DirectoryCMSClient
from django.conf import settings


def create_response(status_code, json_body={}, content=None):
    response = requests.Response()
    response.status_code = status_code
    response.json = lambda: json_body
    response._content = content
    return response


cms_client = DirectoryCMSClient(
    base_url=settings.CMS_URL,
    api_key=settings.CMS_SIGNATURE_SECRET,
)
