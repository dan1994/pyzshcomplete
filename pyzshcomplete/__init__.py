'''
pyzshcomplete supplies completion generation of arbitrary python scripts for
users of zsh. It's written to resemble the interface of argcomplete, a popular
project that provides completion for bash.

In order to use pyzshcomplete, add the following comment at the top of your
script:

```python
# PYTHON_ARGCOMPLETE_OK
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


from os import environ
from sys import exit, stderr
from argparse import ArgumentParser

from pyzshcomplete.adapters.argparse.parser_adapter import ArgparseParserAdapter


__all__ = ['autocomplete']


def autocomplete(parser):
    '''Generates zsh formatted autocompletion for the given parser.'''

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
    return 'PYZSHCOMPLETE' in environ


def _parser_adapter(parser):
    if isinstance(parser, ArgumentParser):
        return ArgparseParserAdapter(parser)

    raise TypeError('The given parser type is not supported by pyzshcomplete')
