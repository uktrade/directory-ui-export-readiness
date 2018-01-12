import csv
import tempfile
import zipfile
from contextlib import contextmanager

import io
import requests
from django.conf import settings
from django.core.management import BaseCommand


REPORTER_AREAS_URL = 'https://comtrade.un.org/data/cache/reporterAreas.json'
API_URL = 'http://comtrade.un.org/api/get/bulk/{type}/{freq}/{ps}/{r}/{px}?token={token}'  # NOQA
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
    'Partner',
    'Partner ISO',
    'Commodity Code',
    'Trade Value'
)
EXCLUDED_COMMODITIES_CODES = (93, )  # Arms


@contextmanager
def open_zipped_csv(file_pointer):
    """
    Enclose all the complicated logic of on-the-fly unzip->csv read in a
    nice context manager.
    """
    with zipfile.ZipFile(file_pointer) as zipped_file:
        # get the first file from zip, assuming it's the only one
        csv_name = zipped_file.filelist[0].filename
        with zipped_file.open(csv_name) as raw_csv_file_pointer:
            # We need to read that as a text IO for CSV reader to work
            csv_fp = io.TextIOWrapper(raw_csv_file_pointer)

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


def stream_to_file_pointer(url, file_pointer):
    """Efficiently stream given url to given file pointer."""
    response = requests.get(url, stream=True)
    for chunk in response.iter_content(chunk_size=4096):
        file_pointer.write(chunk)


def process_row(row):
    """ Process row, yielding a filtered and cleaned row."""
    hs_code = row['Commodity Code']
    has_partner = row['Partner ISO'] != ''
    is_export = row['Trade Flow'] == 'Export'
    is_parent_commodity = len(hs_code) <= 2
    is_allowed_commodity = hs_code not in EXCLUDED_COMMODITIES_CODES
    is_a_country = row['Partner ISO'] != 'WLD'  # exclude world
    if all(
            (has_partner,
             is_export,
             is_parent_commodity,
             is_allowed_commodity,
             is_a_country)
    ):
        yield {
            'Partner': row['Partner'],
            'Partner ISO': row['Partner ISO'],
            'Commodity Code': row['Commodity Code'],
            'Trade Value': row['Trade Value (US$)']
        }


def write_csv(data):
    with open(FILE_NAME, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELD_NAMES)
        writer.writeheader()
        writer.writerows(data)


def get_comtrade_data():
    temporary_file = tempfile.TemporaryFile
    params = {
        'freq': 'A',
        'r': 826,  # United Kingdom
        'ps': 2016,
        'type': 'C',  # Commodities
        'px': 'HS',
        'token': TOKEN
    }
    url = API_URL.format(**params)
    filtered_rows = iter_and_filter_csv_from_url(url, temporary_file)
    return filtered_rows


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING(
                'Downloading and filtering COMTRADE data this may take a while'
            )
        )

        data = get_comtrade_data()
        write_csv(data)

        self.stdout.write(
            self.style.SUCCESS(
                'CSV file generated'
            )
        )
