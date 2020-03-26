from pytest import mark, skip
from sys import version_info
from argparse import REMAINDER


def test_empty(empty_parser, autocomplete_and_compare):
    autocomplete_and_compare(empty_parser, [''])


def test_default(default_parser, autocomplete_and_compare):
    autocomplete_and_compare(default_parser, [
        r'(* : -){-h,--help}[show this help message and exit]'
    ])


@mark.parametrize('action', ['store', 'store_const', 'store_true', 'store_false', 'append', 'append_const', 'count', 'help', 'version', 'extend'])
def test_positional(empty_parser, autocomplete_and_compare, action):
    if action == 'extend' and version_info.minor < 8:
        skip('3.8')

    empty_parser.add_argument('pos', help='A positional argument')
    autocomplete_and_compare(
        empty_parser, [r':pos - A positional argument:_default'])


@mark.parametrize('nargs', [None, 1])
def test_positional_with_one_subargument(empty_parser,
                                         autocomplete_and_compare, nargs):
    empty_parser.add_argument('arg', nargs=nargs)
    autocomplete_and_compare(empty_parser, [
        r':arg:_default'
    ])


def test_positional_with_optional_subargument(empty_parser,
                                              autocomplete_and_compare):
    empty_parser.add_argument('arg', nargs='?')
    autocomplete_and_compare(empty_parser, [
        r'::arg:_default'
    ])


@mark.parametrize('nargs', [2, 10])
def test_positional_with_multiple_subarguments(empty_parser,
                                               autocomplete_and_compare, nargs):
    empty_parser.add_argument('arg', nargs=nargs)
    autocomplete_and_compare(empty_parser, nargs * [
        r':arg:_default'
    ])


@mark.parametrize('nargs', ['*', '+', REMAINDER])
def test_positional_with_variable_subarguments(empty_parser,
                                               autocomplete_and_compare, nargs):
    empty_parser.add_argument('arg', nargs=nargs)
    autocomplete_and_compare(empty_parser, [
        r'*:arg:_default'
    ])


def test_flag(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('-o', help='An optional argument')
    autocomplete_and_compare(empty_parser, [
        r'(-o){-o}+[An optional argument]: :_default'
    ])
