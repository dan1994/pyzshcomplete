'''
pyzshcomplete supplies completion generation of arbitrary python scripts for
users of zsh. It's written to resemble the interface of argcomplete, a popular
project that provides completion for bash.

In order to use pyzshcomplete, add the following comment at the top of your
script:

```python
# PYZSHCOMPLETE_OK
```

then, after your parser is defined, and before the actual parsing is done, add a
call to the autocomplete function like so:

```python
parser = ArgumentParser()
parser.add_argument(...)
...
autocomplete(parser)
args = parser.parse_args()
```
'''


from os import environ, fdopen
from sys import exit
from argparse import ArgumentParser

from pyzshcomplete.adapters.argparse.parser_adapter import ArgparseParserAdapter


__all__ = ['autocomplete']

COMPLETION_CONTEXT_ENVIRONMENT_VARIABLE = 'PYZSHCOMPLETE'
COMPLETION_CONTEXT_OUTPUT_FD = 8
COMPLETION_CONTEXT_ERROR_FD = 9


def autocomplete(parser):
    '''Generates zsh formatted autocompletion for the given parser.'''

    if not _running_in_autocompletion_context():
        return

    output_stream, error_stream = _get_streams()

    try:
        arguments_as_string = _autocomplete(parser)
    except TypeError as e:
        error_stream.write(e)
        exit(-1)

    output_stream.write(arguments_as_string)

    found_arguments = 0 if len(arguments_as_string) > 0 else -1
    exit(found_arguments)


def _running_in_autocompletion_context():
    return COMPLETION_CONTEXT_ENVIRONMENT_VARIABLE in environ


def _get_streams():
    try:
        return fdopen(COMPLETION_CONTEXT_OUTPUT_FD, 'w'), \
            fdopen(COMPLETION_CONTEXT_ERROR_FD, 'w')
    except:
        exit(-1)


def _autocomplete(parser):
    '''This function returns the completions as a string. This allows easier
    testing without having to capture output streams.'''

    parser_adapter = _parser_adapter(parser)
    return str(parser_adapter)


def _parser_adapter(parser):
    if isinstance(parser, ArgumentParser):
        return ArgparseParserAdapter(parser)

    raise TypeError('The given parser type is not supported by pyzshcomplete')
