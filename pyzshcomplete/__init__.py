from os import environ
from sys import exit

from pyzshcomplete.adapters.argparse.parser_adapter import ArgparseParserAdapter


__all__ = ['autocomplete']


def autocomplete(parser):
    if not _running_in_autocompletion_context():
        return

    parser = ArgparseParserAdapter(parser)
    arguments_as_string = str(parser)
    print(arguments_as_string)

    found_arguments = 0 if len(arguments_as_string) > 0 else -1
    exit(found_arguments)


def _running_in_autocompletion_context():
    return 'ARGCOMPLETE' in environ
