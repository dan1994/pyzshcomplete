from pytest import mark, skip
from sys import version_info
from argparse import REMAINDER


@mark.parametrize('action', ['store', 'store_const', 'store_true',
                             'store_false', 'append', 'append_const', 'count',
                             'help', 'version', 'extend'])
def test_actions(empty_parser, autocomplete_and_compare, action):
    if action == 'extend' and version_info.minor < 8:
        skip('3.8')

    empty_parser.add_argument('pos', help='A positional argument')
    autocomplete_and_compare(
        empty_parser, [r':pos - A positional argument:_default'])


@mark.parametrize('nargs', [None, 1])
def test_one_subargument(empty_parser, autocomplete_and_compare, nargs):
    empty_parser.add_argument('arg', nargs=nargs)
    autocomplete_and_compare(empty_parser, [
        r':arg:_default'
    ])


def test_optional_subargument(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('arg', nargs='?')
    autocomplete_and_compare(empty_parser, [
        r'::arg:_default'
    ])


@mark.parametrize('nargs', [2, 10])
def test_multiple_subarguments(empty_parser, autocomplete_and_compare, nargs):
    empty_parser.add_argument('arg', nargs=nargs)
    autocomplete_and_compare(empty_parser, nargs * [
        r':arg:_default'
    ])


@mark.parametrize('nargs', ['*', '+', REMAINDER])
def test_variable_subarguments(empty_parser, autocomplete_and_compare, nargs):
    empty_parser.add_argument('arg', nargs=nargs)
    autocomplete_and_compare(empty_parser, [
        r'*:arg:_default'
    ])


@mark.parametrize('choices', [[], ['choice1'], ['choice1', 'choise2'],
                              ['A choice that needs escaping because it has '
                               'spaces and :']])
def test_choices(empty_parser, autocomplete_and_compare, choices):
    choices_as_str = ' '.join([choice.replace(r':', r'\:').replace(r' ', r'\ ')
                               for choice in choices])

    empty_parser.add_argument('arg', choices=choices)
    autocomplete_and_compare(empty_parser, [
        r':arg:({})'.format(choices_as_str)
    ])


def test_empty_help(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('arg', help='')
    autocomplete_and_compare(empty_parser, [
        r':arg:_default'
    ])


@mark.parametrize('help', ['Help about argument', 'help: argument description'])
def test_help(empty_parser, autocomplete_and_compare, help):
    help_as_str = help.replace(r':', r'\:')

    empty_parser.add_argument('arg', help=help)
    autocomplete_and_compare(empty_parser, [
        r':arg - {}:_default'.format(help_as_str)
    ])


def test_metavar(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('arg', metavar='name')
    autocomplete_and_compare(empty_parser, [
        r':name:_default'
    ])
