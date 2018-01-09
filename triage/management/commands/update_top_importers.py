import requests
from django.conf import settings
from django.core.management import BaseCommand
from django.utils.functional import cached_property


HS_CODES_URL = 'https://comtrade.un.org/data/cache/classificationHS.json'
REPORTER_AREAS_URL = 'https://comtrade.un.org/data/cache/reporterAreas.json'
TRADE_REGIME_FLOW = 'https://comtrade.un.org/data/cache/tradeRegimes.json'
BASE_API_URL = 'http://comtrade.un.org/api/get/bulk/{type}/{freq}/{ps}/{r}/{px}?{token}'  # NOQA
FILE_NAME = 'triage/resources/country_commodity_top_tens.csv'
TOKEN = settings.COMTRADE_API_TOKEN


class Command(BaseCommand):

    def handle(self, *args, **options):
        pass

    def get_data(self):
        params = {
            'freq': 'A',
            'r': self.uk_area_code,
            'ps': 2006,
            'type': 'C',  # Commodities
            'px': 'HS',
            'toke': TOKEN
        }
        url = BASE_API_URL.format(**params)
        response = requests.get(url=url)

    @cached_property
    def countries(self):
        response = requests.get(REPORTER_AREAS_URL)
        self.stdout.write(self.style.SUCCESS('Countries list downloaded'))
        results = response.json()['results']
        return list(filter(lambda x: x['text'] != 'All', results))

    @cached_property
    def export_rg_code(self):
        response = requests.get(TRADE_REGIME_FLOW)
        results = response.json()['results']
        return list(filter(lambda x: x['text'] == 'Export', results))[0]['id']

    @cached_property
    def uk_area_code(self):
        countries = self.countries
        area = list(filter(lambda x: x['text'] == 'United Kingdom', countries))
        return area[0]['id']
