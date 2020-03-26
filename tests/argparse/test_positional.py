from pytest import mark, skip
from sys import version_info
from argparse import REMAINDER


@mark.parametrize('action', ['store', 'append', 'extend'])
def test_actions_with_argument(empty_parser, autocomplete_and_compare, action):
    if action == 'extend' and version_info.minor < 8:
        skip('The extend action is supported from python >= 3.8')

    empty_parser.add_argument('arg', action=action)
    autocomplete_and_compare(empty_parser, [r':arg:_files'])


@mark.parametrize('action', ['store_const', 'append_const'])
def test_actions_without_argument_requiring_const(empty_parser,
                                                  autocomplete_and_compare,
                                                  action):
    empty_parser.add_argument('arg', action=action, const=1)
    autocomplete_and_compare(empty_parser, [r''])


@mark.parametrize('action', ['store_true', 'store_false', 'count'])
def test_actions_without_argument_requiring_no_const(empty_parser,
                                                     autocomplete_and_compare,
                                                     action):
    empty_parser.add_argument('arg', action=action)
    autocomplete_and_compare(empty_parser, [r''])


@mark.parametrize('nargs', [None, 1])
def test_one_subargument(empty_parser, autocomplete_and_compare, nargs):
    empty_parser.add_argument('arg', nargs=nargs)
    autocomplete_and_compare(empty_parser, [r':arg:_files'])


def test_optional_subargument(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('arg', nargs='?')
    autocomplete_and_compare(empty_parser, [r'::arg:_files'])


@mark.parametrize('nargs', [2, 10])
def test_multiple_subarguments(empty_parser, autocomplete_and_compare, nargs):
    empty_parser.add_argument('arg', nargs=nargs)
    autocomplete_and_compare(empty_parser, nargs * [r':arg:_files'])


@mark.parametrize('nargs', ['*', '+', REMAINDER])
def test_variable_subarguments(empty_parser, autocomplete_and_compare, nargs):
    empty_parser.add_argument('arg', nargs=nargs)
    autocomplete_and_compare(empty_parser, [r'*:arg:_files'])


@mark.parametrize('arg_type', [int, float, complex])
def test_types_to_not_complete(empty_parser, autocomplete_and_compare,
                               arg_type):
    empty_parser.add_argument('arg', type=arg_type)
    autocomplete_and_compare(empty_parser, [r':arg: '])


@mark.parametrize('choices', [[], ['choice1'], ['choice1', 'choise2'],
                              ['A choice that needs escaping because it has '
                               'spaces and :']])
def test_choices(empty_parser, autocomplete_and_compare, choices):
    choices_as_str = ' '.join([choice.replace(r':', r'\:').replace(r' ', r'\ ')
                               for choice in choices])

    empty_parser.add_argument('arg', choices=choices)
    autocomplete_and_compare(
        empty_parser, [r':arg:({})'.format(choices_as_str)])


def test_empty_help(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('arg', help='')
    autocomplete_and_compare(empty_parser, [r':arg:_files'])


@mark.parametrize('help', ['Help about argument', 'help: argument description',
                           'help with\nnewlines'])
def test_help(empty_parser, autocomplete_and_compare, help):
    help_as_str = help.replace(r':', r'\:').replace('\n', ' ')

    empty_parser.add_argument('arg', help=help)
    autocomplete_and_compare(
        empty_parser, [r':arg - {}:_files'.format(help_as_str)])


def test_metavar(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('arg', metavar='name')
    autocomplete_and_compare(empty_parser, [r':name:_files'])
