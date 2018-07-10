import abc
import http
import itertools
import csv
from collections import defaultdict
from functools import partial
from operator import itemgetter
from urllib.parse import urljoin

from directory_ch_client.company import CompanyCHClient
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
        if settings.FEATURE_FLAGS['INTERNAL_CH_ON']:
            companies_house_client = CompanyCHClient(
                base_url=settings.INTERNAL_CH_BASE_URL,
                api_key=settings.INTERNAL_CH_API_KEY
            )
            return companies_house_client.search_companies(
                query=term
            )
        else:
            url = cls.endpoints['search']
            return cls.get(url, params={'q': term})


class BaseCSVComtradeFile(abc.ABC):
    file_path = abc.abstractproperty()

    @abc.abstractmethod
    def format_csv_rows(self):
        return {}

    @classmethod
    def load_csv_rows(cls):
        with open(cls.file_path) as f:
            reader = csv.DictReader(f)
            reader.fieldnames = [
                item.lower().replace(' ', '_') for item in reader.fieldnames
            ]
            return list(reader)

    @classmethod
    def read(cls):
        return cls.format_csv_rows()


class CountryCommodityCSVComtradeFile(BaseCSVComtradeFile):
    file_path = 'triage/resources/country_commodity_top_tens.csv'

    @classmethod
    def format_csv_rows(cls):
        csv_rows = cls.load_csv_rows()
        sorted_csv_rows = sorted(
            csv_rows,
            key=lambda row: (row["commodity_code"], 0-int(row['trade_value']))
        )
        grouped_lines = itertools.groupby(
            sorted_csv_rows,
            key=lambda row: row['commodity_code']
        )
        return {'HS' + key: list(group) for key, group in grouped_lines}


class CountryCSVComtradeFile(BaseCSVComtradeFile):
    file_path = 'triage/resources/countries.csv'

    @classmethod
    def format_csv_rows(cls):
        csv_rows = cls.load_csv_rows()
        for row in csv_rows:
            gdp = row['gdp'].replace(',', '').replace(' ', '')
            if gdp.isdigit():
                row['gdp'] = int(gdp) * 1000000
            else:
                row['gdp'] = 0
        return {row['country_code']: row for row in csv_rows}


class CountryExportTotalsCSVComtradeFile(BaseCSVComtradeFile):
    file_path = 'triage/resources/country_commodity_export_totals.csv'

    @classmethod
    def format_csv_rows(cls):
        csv_rows = cls.load_csv_rows()
        formatted = defaultdict(dict)
        for row in csv_rows:
            harmonised_system_code = 'HS' + row['commodity_code']
            country_code = row['partner_iso']
            trade_value = row['trade_value']
            formatted[harmonised_system_code][country_code] = trade_value
        return formatted


def get_top_markets(commodity_code):

    top_markets = CountryCommodityCSVComtradeFile.read()
    countries_data = CountryCSVComtradeFile.read()
    global_trade_value = CountryExportTotalsCSVComtradeFile().read()
    markets = top_markets[commodity_code]

    for market in markets:
        country_code = market['partner_iso']
        market['country'] = countries_data.get(country_code)
        market['global_trade_value'] = int(
            global_trade_value[commodity_code][country_code]
        )
    return markets


def get_top_importer(commodity_code):
    data = get_top_markets(commodity_code)
    top = sorted(data, key=itemgetter('global_trade_value'), reverse=True)[0]
    return {
        'partner': top['partner'],
        'global_trade_value': top['global_trade_value'],
        'uk_export_value': sum(int(i['trade_value']) for i in data),
    }
