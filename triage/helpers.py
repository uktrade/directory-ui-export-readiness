import abc
import http
from functools import partial
from urllib.parse import urljoin

from django.conf import settings
import requests

from api_client import api_client


class BaseTriageAnswersManager(abc.ABC):
    def __init__(self, request):
        self.request = request

    persist_answers = abc.abstractproperty()
    retrieve_answers = abc.abstractproperty()


class TriageAnswersManager:
    def __new__(cls, request):
        if request.sso_user is None:
            return SessionTriageAnswersManager(request)
        return DatabaseTriageAnswersManager(request)


class SessionTriageAnswersManager(BaseTriageAnswersManager):
    SESSION_KEY = 'TRIAGE_ANSWERS'

    def persist_answers(self, answers):
        session = self.request.session
        session[self.SESSION_KEY] = answers
        session.modified = True

    def retrieve_answers(self):
        return self.request.session.get(self.SESSION_KEY, {})


class DatabaseTriageAnswersManager(BaseTriageAnswersManager):

    def persist_answers(self, answers):
        if self.retrieve_answers():
            api_client_method = api_client.exportreadiness.update_triage_result
        else:
            api_client_method = api_client.exportreadiness.create_triage_result
        response = api_client_method(
            form_data=answers,
            sso_session_id=self.request.sso_user.session_id,
        )
        response.raise_for_status()

    def retrieve_answers(self):
        response = api_client.exportreadiness.retrieve_triage_result(
            sso_session_id=self.request.sso_user.session_id
        )
        if response.status_code == 404:
            return {}
        response.raise_for_status()
        return response.json()


class CompaniesHouseClient:

    api_key = settings.COMPANIES_HOUSE_API_KEY
    make_api_url = partial(urljoin, 'https://api.companieshouse.gov.uk')
    endpoints = {
        'search': make_api_url('search/companies'),
    }
    session = requests.Session()

    @classmethod
    def get_auth(cls):
        return requests.auth.HTTPBasicAuth(cls.api_key, '')

    @classmethod
    def get(cls, url, params={}):
        response = cls.session.get(url=url, params=params, auth=cls.get_auth())
        if response.status_code == http.client.UNAUTHORIZED:
            response.raise_for_status()
        return response

    @classmethod
    def search(cls, term):
        url = cls.endpoints['search']
        return cls.get(url, params={'q': term})
