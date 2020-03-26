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
