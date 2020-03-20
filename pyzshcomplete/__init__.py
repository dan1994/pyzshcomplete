from os import environ
from sys import exit, stderr
from argparse import ArgumentParser

from pyzshcomplete.adapters.argparse.parser_adapter import ArgparseParserAdapter


__all__ = ['autocomplete']


def autocomplete(parser):
    if not _running_in_autocompletion_context():
        return

    try:
        parser_adapter = _parser_adapter(parser)
    except TypeError as e:
        stderr.write(e)

    arguments_as_string = str(parser_adapter)
    print(arguments_as_string)

    found_arguments = 0 if len(arguments_as_string) > 0 else -1
    exit(found_arguments)


def _running_in_autocompletion_context():
    return 'ARGCOMPLETE' in environ


def _parser_adapter(parser):
    if isinstance(parser, ArgumentParser):
        return ArgparseParserAdapter(parser)

    raise TypeError('The given parser type is not supported by pyzshcomplete')
