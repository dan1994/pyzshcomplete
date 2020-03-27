# pyzshcomplete

Tab completion for arbitraty `python` scripts in `zsh`.

![pyzshcomplete_example](https://user-images.githubusercontent.com/6225230/77791128-273dc480-7077-11ea-81b4-ea34fd9251a2.PNG)

## Introduction

This project was inspired by
[`argcomplete`](https://github.com/kislyuk/argcomplete), which supplies argument
completion for `bash`.

While having a workaround for `zsh` (which just enables compatibility for `bash`
completion scripts), `argcomplete` can't use the full power of the `zsh`
completion system (e.g. show flag help messages).

`pyzshcomplete` was written to utilize as many of the features offered by `zsh`
as possible.

## Installation

# TODO - Finalize installation details

```zsh
pip install pyzshcomplete
```

Restart `zsh` after the installation is complete.

## Usage

To emphasize the similarity to `argcomplete`, here is the example usage shown in
the `argcomplete` readme:

```python
#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import argcomplete, argparse
parser = argparse.ArgumentParser()
...
argcomplete.autocomplete(parser)
args = parser.parse_args()
...
```

And here it is adapted to `pyzshcomplete`:

```python
#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import pyzshcomplete, argparse
parser = argparse.ArgumentParser()
...
pyzshcomplete.autocomplete(parser)
args = parser.parse_args()
...
```

Note that the magic string `PYTHON_ARGCOMPLETE_OK` is required to appear at the
top of the script exactly like in `argcomplete`.

As to the `autocomplete` method, I'll just quote `argcomplete`:

> ### argcomplete.autocomplete(_parser_)
>
> This method is the entry point to the module. It must be called **after**
> ArgumentParser construction is complete, but **before** the
> `ArgumentParser.parse_args()` method is called. The method looks for an
> environment variable that the completion hook shellcode sets, and if it's
> there, collects completions, prints them to the output stream (fd 8 by
> default), and exits. Otherwise, it returns to the caller immediately.
>
> #### Side effects
>
> Argcomplete gets completions by running your program. It intercepts the
> execution flow at the moment `argcomplete.autocomplete()` is called. After
> sending completions, it exits using `exit_method` (`os._exit` by default).
> This means if your program has any side effects that happen before
> `argcomplete `is called, those side effects will happen every time the user
> presses `<TAB>` (although anything your program prints to stdout or stderr
> will be suppressed). For this reason it's best to construct the argument
> parser and call `argcomplete.autocomplete()` as early as possible in your
> execution flow.
>
> #### Performance
>
> If the program takes a long time to get to the point where
> `argcomplete.autocomplete()` is called, the tab completion process will feel
> sluggish, and the user may lose confidence in it. So it's also important to
> minimize the startup time of the program up to that point (for example, by
> deferring initialization or importing of large modules until after parsing
> options).

The only difference is that in `pyzshcomplete` the exit method is `sys.exit` and
it is not configurable.

### Can I use both `argcomplete` and `pyzshcomplete`?

TL;DR: **Yes!**

example:

```python
#!/usr/bin/env python3

from argparse import ArgumentParser
import pyzshcomplete, argcomplete

parser = ArgumentParser()
parser.add_argument('arg')

# These lines can be in any order
argcomplete.autocomplete(parser)
pyzshcomplete.autocomplete(parser)

args = parser.parse_args()
```

Both `argcomplete` and `pyzshcomplete` use an environment variable set by the
completion script that is unique to that shell. If that variable is not set,
the `autocomplete` function simply returns without doing anything.

`argcomplete` uses `_ARGCOMPLETE` and `pyzshcomplete` uses `PYZSHCOMPLETE`. this
means that if you're using `bash`, the `_ARGCOMPLETE` environment variable will
be set, and only `argcomplete.autocomplete` will do completion magic, and vice
versa if you're using `zsh`.

### Smart Completion

`zsh` offers easy ways to complete things such as process ids, user accounts,
network interfaces, bookmarks and more.

As of this moment, there is no mechanism that enables associating an argument
with these options. Stay tuned, as it is a prioritized feature.

## Supported Parsers

`pyzshcomplete` was written to be easy to extend for new parsers. It currently
supports only `argparse`, but you are welcome to request or contribute support
for other parsers.

## Non-Supported Features

Some features of certain parsers can't be (easily enough) supported by `zsh` or
`pyzshcomplete` and are listed here for public knowledge.

### Argparse

- **Subparsers** - Subparsers **will** be supported in the near future.
- Custom actions - There is no way to know in advance what effect will actions
have on the way the argument should be supplied (e.g. can a flag be specified
multiple times?).
- Non-standard flag prefixes - Only the `-` and `+` prefixes are supported, as
that is what the `_arguments` completion utility supports.
- Usage of the `from_file_prefix_chars` in `ArgumentParser`

## Python Support

Official support is for Python 3 only.

## Feature Requests and Bug Reports

Feature requests and bug reports are tracked on
[Github](https://github.com/dan1994/pyzshcomplete/issues).

## Resources

Getting into `zsh` internals isn't easy. If you are interested to learn more of
the inner workings, take a look at the following resources:

- From Bash to Z Shell - This book is intended to teach `zsh` by example, and is
much more easy to read than any manual or user guide I've encountered (You can
find the full pdf in a simple search, but I didn't tell you that).
- [The `Zsh` Manual](http://zsh.sourceforge.net/Doc/zsh_a4.pdf) - After you've
acquainted yourself with the basics, and want the full spec of anything
particular, this is the document to go to.
- [`Zsh` Reference Card](http://www.bash2zsh.com/zsh_refcard/refcard.pdf) -
After you know what you're doing, you can use this reference card for quick
reminders.

## License

Licensed under the terms of the MIT License.
