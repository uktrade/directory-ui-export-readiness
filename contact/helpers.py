from directory_api_client.client import api_client
import requests.exceptions

from django.conf import settings


def retrieve_exporting_advice_email(postcode):
    try:
        office_details = retrieve_regional_office(postcode)
    except requests.exceptions.RequestException:
        email = settings.CONTACT_DIT_AGENT_EMAIL_ADDRESS
    else:
        email = office_details['email']
    return email


def retrieve_regional_office(postcode):
    response = api_client.exporting.lookup_regional_office_by_postcode(
        postcode
    )
    response.raise_for_status()
    return response.json()


def get_company_profile(request):
    if request.sso_user:
        response = api_client.company.retrieve_private_profile(
            sso_session_id=request.sso_user.session_id,
        )
        if response.status_code == 200:
            return response.json()
