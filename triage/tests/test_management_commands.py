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
    with open('triage/tests/comtrade_test.zip', 'r') as test_file:
        mocked_requests.get.return_value.iter_content.return_value = \
            stream_file_in_chucks(test_file)
        call_command('update_top_importers')
        assert mocked_write_csv.called is True
        data = mocked_write_csv.call_args[0][0]
        assert isinstance(
            data, types.GeneratorType
        )
