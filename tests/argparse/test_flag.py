from pytest import mark, skip
from sys import version_info


def test_short_option(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('-a')
    autocomplete_and_compare(empty_parser, [r'(-a){-a}+: :_default'])


def test_long_option(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('--arg')
    autocomplete_and_compare(empty_parser, [r'(--arg){--arg}+: :_default'])


def test_short_and_long_option(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('-a', '--arg')
    autocomplete_and_compare(
        empty_parser, [r'(-a --arg){-a,--arg}+: :_default'])


@mark.parametrize('action', ['store'])
def test_non_repeating_actions_with_argument(empty_parser,
                                             autocomplete_and_compare, action):
    empty_parser.add_argument('-a', action=action)
    autocomplete_and_compare(empty_parser, [r'(-a){-a}+: :_default'])


@mark.parametrize('action', ['append', 'extend'])
def test_repeating_actions_with_argument(empty_parser, autocomplete_and_compare,
                                         action):
    if action == 'extend' and version_info.minor < 8:
        skip('The extend action is supported from python >= 3.8')

    empty_parser.add_argument('-a', action=action)
    autocomplete_and_compare(empty_parser, [r'*{-a}+: :_default'])


@mark.parametrize('action', ['store_const'])
def test_non_repeating_actions_without_argument_requiring_const(empty_parser,
                                                                autocomplete_and_compare,
                                                                action):
    empty_parser.add_argument('-a', action=action, const=1)
    autocomplete_and_compare(empty_parser, [r'(-a){-a}'])


@mark.parametrize('action', ['append_const'])
def test_repeating_actions_without_argument_requiring_const(empty_parser,
                                                            autocomplete_and_compare,
                                                            action):
    empty_parser.add_argument('-a', action=action, const=1)
    autocomplete_and_compare(empty_parser, [r'*{-a}'])


@mark.parametrize('action', ['store_true', 'store_false'])
def test_non_repeating_actions_without_argument_requiring_no_const(empty_parser,
                                                                   autocomplete_and_compare,
                                                                   action):
    empty_parser.add_argument('-a', action=action)
    autocomplete_and_compare(empty_parser, [r'(-a){-a}'])


@mark.parametrize('action', ['count'])
def test_repeating_actions_without_argument_requiring_no_const(empty_parser,
                                                               autocomplete_and_compare,
                                                               action):
    empty_parser.add_argument('-a', action=action)
    autocomplete_and_compare(empty_parser, [r'*{-a}'])


def test_help_action(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('-a', action='help')
    autocomplete_and_compare(empty_parser, [r'(* : -){-a}'])


def test_version_action(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('-a', action='version')
    # The version action sets the help message if it's None
    autocomplete_and_compare(
        empty_parser, [r"(* : -){-a}[show program's version number and exit]"])
