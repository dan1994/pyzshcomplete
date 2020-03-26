from pytest import fixture, raises
from argparse import ArgumentParser
from io import StringIO
import os
import sys

from pyzshcomplete import autocomplete


sys.path.append('../pyzshcomplete')

os.environ['PYZSHCOMPLETE'] = '1'


@fixture(scope='function')
def default_parser():
    return ArgumentParser()


@fixture(scope='function')
def empty_parser():
    return ArgumentParser(add_help=False)


@fixture(scope='function')
def autocomplete_and_compare(capsys):
    def _autocomplete_and_compare(parser, expected):
        with raises(SystemExit):
            autocomplete(parser)
        output = capsys.readouterr().out
        options = output.split('\n')[:-1]
        assert sorted(options) == sorted(expected)

    return _autocomplete_and_compare
