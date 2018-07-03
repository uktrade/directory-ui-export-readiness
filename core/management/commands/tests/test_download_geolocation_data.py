import os
import tarfile
from unittest.mock import patch

from requests.exceptions import HTTPError
import requests_mock
import pytest

from django.core.management import call_command

from core.management.commands.download_geolocation_data import (
    GeolocationArchive
)


@pytest.fixture
def archive_missing_database(settings):
    file_path = os.path.join(
        settings.PROJECT_ROOT,
        '../core/management/commands/tests/with-missing-database-file.tar.gz'
    )
    with open(file_path, 'rb') as f:
        return GeolocationArchive(f.read())


@pytest.fixture
def archive_with_database(settings):
    file_path = os.path.join(
        settings.PROJECT_ROOT,
        '../core/management/commands/tests/with-database-file.tar.gz'
    )
    with open(file_path, 'rb') as f:
        return GeolocationArchive(f.read())


def test_handles_not_ok_response(settings):
    with requests_mock.mock() as mock:
        mock.get(
            settings.GEOLOCATION_MAXMIND_DATABASE_FILE_URL,
            status_code=400
        )
        with pytest.raises(HTTPError):
            call_command('download_geolocation_data')


def test_handles_url_not_archive(settings):
    with requests_mock.mock() as mock:
        mock.get(
            settings.GEOLOCATION_MAXMIND_DATABASE_FILE_URL,
            status_code=200,
            content=b'hello',
        )

        with pytest.raises(tarfile.ReadError):
            call_command('download_geolocation_data')


@patch.object(GeolocationArchive, 'from_url')
def test_handles_missing_database_file(
    mock_from_url, archive_missing_database
):
    mock_from_url.return_value = archive_missing_database

    with pytest.raises(ValueError):
        call_command('download_geolocation_data')


@patch.object(GeolocationArchive, 'from_url')
def test_handles_database_file(
    mock_from_url, archive_with_database, settings
):
    settings.GEOIP_COUNTRY = 'GeoLite2-Country-test.mmdb'
    expected_path = os.path.join(settings.GEOIP_PATH, settings.GEOIP_COUNTRY)
    assert os.path.isfile(expected_path) is False

    mock_from_url.return_value = archive_with_database

    call_command('download_geolocation_data')

    assert os.path.isfile(expected_path) is True
    os.remove(expected_path)
