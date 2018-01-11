import types
from unittest.mock import patch

from django.core.management import call_command


def stream_file_in_chucks(file_object):
    while True:
        data = file_object.read(4096)
        if not data:
            break
        yield data


@patch('triage.management.commands.update_top_importers.write_csv')
@patch('triage.management.commands.update_top_importers.requests')
def test_update_top_importers_write_csv(
        mocked_requests,
        mocked_write_csv
):
    with open('triage/tests/comtrade_test.zip', 'rb') as test_file:
        mocked_requests.get.return_value.iter_content.return_value = \
            stream_file_in_chucks(test_file)
        call_command('update_top_importers')
        assert mocked_write_csv.called is True
        data = mocked_write_csv.call_args[0][0]
        assert isinstance(
            data, types.GeneratorType
        )
        expected_data = [
            {
                'Partner': 'Antigua and Barbuda',
                'Partner ISO': 'ATG',
                'Commodity Code': '01',
                'Trade Value': '2703'
            }, {
                'Partner': 'Azerbaijan',
                'Partner ISO': 'AZE',
                'Commodity Code': '01',
                'Trade Value': '148262'
            }, {
                'Partner': 'Argentina',
                'Partner ISO': 'ARG',
                'Commodity Code': '93',
                'Trade Value': '88427'
            }, {
                'Partner': 'Australia',
                'Partner ISO': 'AUS',
                'Commodity Code': '01',
                'Trade Value': '25152614'
            }
        ]
        assert list(data) == expected_data
