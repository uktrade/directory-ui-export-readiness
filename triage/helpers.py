import abc

from api_client import api_client


class BaseTriageAnswersManager(abc.ABC):
    def __init__(self, request):
        self.request = request

    persist_answers = abc.abstractproperty()
    retrieve_answers = abc.abstractproperty()


class TriageAnswersManager:
    def __new__(self, request):
        if request.sso_user is None:
            return SessionTriageAnswersManager(request)
        return DatabaseTriageAnswersManager(request)


class SessionTriageAnswersManager(BaseTriageAnswersManager):
    SESSION_KEY = 'TRIAGE_ANSWERS'

    def persist_answers(self, answers):
        self.request.session[self.SESSION_KEY] = answers

    def retrieve_answers(self):
        return self.request.session.get(self.SESSION_KEY, {})


class DatabaseTriageAnswersManager(BaseTriageAnswersManager):

    def persist_answers(self, answers):
        response = api_client.exportreadiness.create_triage_result(
            form_data=answers,
            sso_session_id=self.request.sso_user.session_id,
        )
        response.raise_for_status()

    def retrieve_answers(self):
        response = api_client.exportreadiness.retrieve_triage_result(
            sso_session_id=self.request.sso_user.session_id
        )
        response.raise_for_status()
        return response.json()
