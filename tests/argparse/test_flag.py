from pytest import mark, skip
from sys import version_info
from argparse import OPTIONAL, ZERO_OR_MORE, ONE_OR_MORE, REMAINDER


def test_short_option(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('-a')
    autocomplete_and_compare(empty_parser, [r'(-a)-a+: :_files'])


def test_long_option(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('--arg')
    autocomplete_and_compare(empty_parser, [r'(--arg)--arg+: :_files'])


def test_short_and_long_option(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('-a', '--arg')
    autocomplete_and_compare(empty_parser, [
        r'(-a --arg)-a+: :_files',
        r'(-a --arg)--arg+: :_files'
    ])


@mark.parametrize('action', ['store'])
def test_non_repeating_actions_with_argument(empty_parser,
                                             autocomplete_and_compare, action):
    empty_parser.add_argument('-a', action=action)
    autocomplete_and_compare(empty_parser, [r'(-a)-a+: :_files'])


@mark.parametrize('action', ['append', 'extend'])
def test_repeating_actions_with_argument(empty_parser, autocomplete_and_compare,
                                         action):
    if action == 'extend' and version_info.minor < 8:
        skip('The extend action is supported from python >= 3.8')

    empty_parser.add_argument('-a', action=action)
    autocomplete_and_compare(empty_parser, [r'*-a+: :_files'])


@mark.parametrize('action', ['store_const'])
def test_non_repeating_actions_without_argument_requiring_const(empty_parser,
                                                                autocomplete_and_compare,
                                                                action):
    empty_parser.add_argument('-a', action=action, const=1)
    autocomplete_and_compare(empty_parser, [r'(-a)-a'])


@mark.parametrize('action', ['append_const'])
def test_repeating_actions_without_argument_requiring_const(empty_parser,
                                                            autocomplete_and_compare,
                                                            action):
    empty_parser.add_argument('-a', action=action, const=1)
    autocomplete_and_compare(empty_parser, [r'*-a'])


@mark.parametrize('action', ['store_true', 'store_false'])
def test_non_repeating_actions_without_argument_requiring_no_const(empty_parser,
                                                                   autocomplete_and_compare,
                                                                   action):
    empty_parser.add_argument('-a', action=action)
    autocomplete_and_compare(empty_parser, [r'(-a)-a'])


@mark.parametrize('action', ['count'])
def test_repeating_actions_without_argument_requiring_no_const(empty_parser,
                                                               autocomplete_and_compare,
                                                               action):
    empty_parser.add_argument('-a', action=action)
    autocomplete_and_compare(empty_parser, [r'*-a'])


def test_help_action(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('-a', action='help')
    autocomplete_and_compare(empty_parser, [r'(* : -)-a'])


def test_version_action(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('-a', action='version')
    # The version action sets the help message if it's None
    autocomplete_and_compare(
        empty_parser, [r"(* : -)-a[show program's version number and exit]"])


@mark.parametrize('nargs', [None, 1])
def test_one_subargument(empty_parser, autocomplete_and_compare, nargs):
    empty_parser.add_argument('-a', nargs=nargs)
    autocomplete_and_compare(empty_parser, [r'(-a)-a+: :_files'])


def test_optional_subargument(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('-a', nargs=OPTIONAL)
    autocomplete_and_compare(empty_parser, [r'(-a)-a+:: :_files'])


@mark.parametrize('nargs', [2, 10])
def test_multiple_subarguments(empty_parser, autocomplete_and_compare, nargs):
    empty_parser.add_argument('-a', nargs=nargs)
    autocomplete_and_compare(
        empty_parser, [r'(-a)-a{}'.format(nargs * r': :_files')])


@mark.parametrize('nargs', [ZERO_OR_MORE, ONE_OR_MORE, REMAINDER])
def test_variable_subarguments(empty_parser, autocomplete_and_compare, nargs):
    empty_parser.add_argument('-a', nargs=nargs)
    autocomplete_and_compare(empty_parser, [r'(-a)-a+:*: :_files'])


@mark.parametrize('arg_type', [int, float, complex])
def test_types_to_not_complete(empty_parser, autocomplete_and_compare,
                               arg_type):
    empty_parser.add_argument('-a', type=arg_type)
    autocomplete_and_compare(empty_parser, [r'(-a)-a+: : '])


@mark.parametrize('choices', [[], ['choice1'], ['choice1', 'choise2'],
                              ['A choice that needs escaping because it has '
                               'spaces and :']])
def test_choices(empty_parser, autocomplete_and_compare, choices):
    choices_as_str = ' '.join([choice.replace(r':', r'\:').replace(r' ', r'\ ')
                               for choice in choices])

    empty_parser.add_argument('-a', choices=choices)
    autocomplete_and_compare(
        empty_parser, [r'(-a)-a+: :({})'.format(choices_as_str)])


def test_required(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('-a', required=True)
    autocomplete_and_compare(empty_parser, [r'(-a)-a+: :_files'])


def test_empty_help(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('-a', help='')
    autocomplete_and_compare(empty_parser, [r'(-a)-a+: :_files'])


@mark.parametrize('help', ['Help about argument', 'help: argument description',
                           'help with\nnewlines'])
def test_help(empty_parser, autocomplete_and_compare, help):
    help_as_str = help.replace(r':', r'\:').replace('\n', ' ')

    empty_parser.add_argument('-a', help=help)
    autocomplete_and_compare(
        empty_parser, [r'(-a)-a+[{}]: :_files'.format(help_as_str)])


def test_formatted_help(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('-a', nargs='?', const='const', default='default',
                              type=str, choices=['choice1', 'choice2'],
                              required=True, metavar='metavar',
                              help='%(nargs)s %(const)s %(default)s %(type)s '
                              '%(choices)s %(required)s %(metavar)s %(dest)s '
                              '%(help)s')
    autocomplete_and_compare(empty_parser, [
        r"(-a)-a+[? const default <class 'str'> ['choice1', 'choice2'] True "
        r'metavar a %(nargs)s %(const)s %(default)s %(type)s %(choices)s '
        r'%(required)s %(metavar)s %(dest)s %(help)s]:: :(choice1 choice2)'
    ])


def test_metavar(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('-a', metavar='name')
    autocomplete_and_compare(empty_parser, [r'(-a)-a+: :_files'])


def test_dest(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('-a', dest='name')
    autocomplete_and_compare(empty_parser, [r'(-a)-a+: :_files'])
