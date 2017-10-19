import pytest
import requests
import requests_mock

from triage import helpers


def test_search():
    with requests_mock.mock() as mock:
        mock.get(
            'https://api.companieshouse.gov.uk/search/companies',
            status_code=200,
        )
        response = helpers.CompaniesHouseClient.search(term='green')
        assert response.status_code == 200

    request = mock.request_history[0]

    assert request.query == 'q=green'


def test_search_unauthoirized():
    with requests_mock.mock() as mock:
        mock.get(
            'https://api.companieshouse.gov.uk/search/companies',
            status_code=401,
        )
        with pytest.raises(requests.HTTPError):
            helpers.CompaniesHouseClient.search(term='green')
