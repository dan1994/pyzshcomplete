from pyzshcomplete import autocomplete
from pytest import fixture, raises

import os


os.environ['PYZSHCOMPLETE'] = '1'


@fixture(scope='function')
def autocomplete_and_compare(capsys):
    def _autocomplete_and_compare(parser, expected):
        with raises(SystemExit):
            autocomplete(parser)
        output = capsys.readouterr().out
        options = output.split('\n')[:-1]
        assert options == expected

    return _autocomplete_and_compare
