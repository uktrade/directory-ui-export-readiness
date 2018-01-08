import csv
import dbm

from django.core.management import BaseCommand

import requests
from django.utils.functional import cached_property

HS_CODES_URL = 'https://comtrade.un.org/data/cache/classificationHS.json'
REPORTER_AREAS_URL = 'https://comtrade.un.org/data/cache/reporterAreas.json'
TRADE_REGIME_FLOW = 'https://comtrade.un.org/data/cache/tradeRegimes.json'
BASE_API_URL = 'https://comtrade.un.org/api/get'
FILE_NAME = 'triage/resources/country_commodity_top_tens.csv'


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.write_csv(data=self.get_data())

    def get_data(self):
        for country in self.countries:
            for code in self.hs_codes:

                self.stdout.write(
                    self.style.SUCCESS(
                        'Downloading {commodity} for {country}'.format(
                            commodity=code['text'],
                            country=country['text']
                        )
                    )
                )

                payload = {
                    'fmt': 'json',
                    'max': 1,
                    'freq': 'A',
                    'rg': self.export_rg_code,
                    'r': self.uk_area_code,
                    'p': country['id'],
                    'ps': 2006,
                    'type': 'C',  # Commodities
                    'px': 'HS',
                    'cc': code['id']
                }
                response = requests.get(url=BASE_API_URL, params=payload)
                data = response.json()['dataset']
                if data:
                    row = {
                        'Partner ISO': data[0]['ptCode'],
                        'Commodity Code': data[0]['cmdCode'],
                        'Trade Value': data[0]['TradeValue']
                    }
                    yield row

    @cached_property
    def countries(self):
        response = requests.get(REPORTER_AREAS_URL)
        self.stdout.write(self.style.SUCCESS('Countries list downloaded'))
        results = response.json()['results']
        return list(filter(lambda x: x['text'] != 'All', results))

    @cached_property
    def hs_codes(self):
        response = requests.get(HS_CODES_URL)
        self.stdout.write(self.style.SUCCESS('HS codes list downloaded'))
        results = response.json()['results']
        return [code for code in results if code['parent'] == 'TOTAL']

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

    def write_csv(self, data):
        fieldnames = ('Partner ISO', 'Commodity Code', 'Trade Value')
        with open(FILE_NAME, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
