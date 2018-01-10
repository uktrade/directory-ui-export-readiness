import csv
import tempfile
import zipfile
from contextlib import contextmanager

import io
import requests
from django.conf import settings
from django.core.management import BaseCommand
from django.utils.functional import cached_property


HS_CODES_URL = 'https://comtrade.un.org/data/cache/classificationHS.json'
REPORTER_AREAS_URL = 'https://comtrade.un.org/data/cache/reporterAreas.json'
TRADE_REGIME_FLOW = 'https://comtrade.un.org/data/cache/tradeRegimes.json'
BASE_API_URL = 'http://comtrade.un.org/api/get/bulk/{type}/{freq}/{ps}/{r}/{px}?token={token}'  # NOQA
FILE_NAME = 'triage/resources/country_commodity_top_tens.csv'
TOKEN = settings.COMTRADE_API_TOKEN
COMTRADE_CSV_FIELD_NAMES = (
    'Classification',
    'Year',
    'Period',
    'Period Desc.',
    'Aggregate Level',
    'Is Leaf Code',
    'Trade Flow Code',
    'Trade Flow',
    'Reporter Code',
    'Reporter',
    'Reporter ISO',
    'Partner Code',
    'Partner',
    'Partner ISO',
    'Commodity Code',
    'Commodity',
    'Qty Unit Code',
    'Qty Unit',
    'Qty',
    'Netweight (kg)',
    'Trade Value (US$)',
    'Flag'
)
CSV_FIELD_NAMES = (
    'Partner ISO',
    'Commodity Code',
    'Trade Value'
)


@contextmanager
def open_zipped_csv(fp):
    """
    Enclose all the complicated logic of on-the-fly unzip->csv read in a
    nice context manager.
    """
    with zipfile.ZipFile(fp) as zf:
        # get the first file from zip, assuming it's the only one
        csv_name = zf.filelist[0].filename
        with zf.open(csv_name) as raw_csv_fp:
            # We need to read that as a text IO for CSV reader to work
            csv_fp = io.TextIOWrapper(raw_csv_fp)

            yield csv.DictReader(csv_fp, fieldnames=COMTRADE_CSV_FIELD_NAMES)


def iter_and_filter_csv_from_url(url, tmp_file_creator):
    """Fetch & cache zipped CSV, and then iterate though contents."""
    with tmp_file_creator() as tf:
        stream_to_file_pointer(url, tf)
        tf.seek(0, 0)

        with open_zipped_csv(tf) as csv_reader:
            next(csv_reader)  # skip the csv header
            for row in csv_reader:
                yield from process_row(row)


def stream_to_file_pointer(url, fp):
    """Efficiently stream given url to given file pointer."""
    response = requests.get(url, stream=True)
    for chunk in response.iter_content(chunk_size=4096):
        fp.write(chunk)


def process_row(row):
    """ Process row, yielding a filtered and cleaned row."""
    if row['Trade Flow'] == 'Export' and len(row['Commodity Code']) <= 2:
        yield {
            'Partner ISO': row['Partner ISO'],
            'Commodity Code': row['Commodity Code'],
            'Trade Value': row['Trade Value (US$)']
        }


class Command(BaseCommand):

    def handle(self, *args, **options):
        data = self.get_data()
        self.write_csv(data)

    def get_data(self):
        self.stdout.write(
            self.style.SUCCESS(
                'Downloading and filtering COMTRADE data this may take a while'
            )
        )
        temporary_file = tempfile.TemporaryFile
        params = {
            'freq': 'A',
            'r': self.uk_area_code,
            'ps': 2016,
            'type': 'C',  # Commodities
            'px': 'HS',
            'token': TOKEN
        }
        url = BASE_API_URL.format(**params)
        import ipdb; ipdb.set_trace()
        filtered_rows = iter_and_filter_csv_from_url(url, temporary_file)
        return filtered_rows

    @cached_property
    def countries(self):
        response = requests.get(REPORTER_AREAS_URL)
        results = response.json()['results']
        return list(filter(lambda x: x['text'] != 'All', results))

    @cached_property
    def uk_area_code(self):
        countries = self.countries
        area = list(filter(lambda x: x['text'] == 'United Kingdom', countries))
        return area[0]['id']

    @staticmethod
    def write_csv(data):
        with open(FILE_NAME, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELD_NAMES)
            writer.writeheader()
            writer.writerows(data)
