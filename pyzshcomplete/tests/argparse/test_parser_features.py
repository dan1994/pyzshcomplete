from argparse import ArgumentParser


def test_parents(autocomplete_and_compare):
    parent = ArgumentParser(add_help=False)
    parent.add_argument('arg')
    child = ArgumentParser(parents=[parent], add_help=False)
    child.add_argument('-a')
    autocomplete_and_compare(child, [
        r':arg:_files',
        r'(-a)-a+: :_files'
    ])


def test_groups(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('arg_a')
    group = empty_parser.add_argument_group()
    group.add_argument('arg_b')
    autocomplete_and_compare(empty_parser, [
        r':arg_a:_files',
        r':arg_b:_files'
    ])


def test_mutually_exclusive_groups(empty_parser, autocomplete_and_compare):
    group = empty_parser.add_mutually_exclusive_group()
    group.add_argument('-a')
    group.add_argument('-b', action='append')
    autocomplete_and_compare(empty_parser, [
        r'(-a -b)-a+: :_files',
        r'(-a)*-b+: :_files'
    ])
