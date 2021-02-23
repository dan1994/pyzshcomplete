#############
pyzshcomplete
#############

.. image:: https://github.com/dan1994/pyzshcomplete/workflows/Tests/badge.svg
   :target: https://github.com/dan1994/pyzshcomplete/workflows/Tests/badge.svg
.. image:: https://github.com/dan1994/pyzshcomplete/workflows/Code%20Scanning/badge.svg
   :target: https://github.com/dan1994/pyzshcomplete/workflows/Code%20Scanning/badge.svg

----

Tab completion for arbitraty ``python`` scripts in ``zsh``.

.. image:: https://user-images.githubusercontent.com/6225230/77791128-273dc480-7077-11ea-81b4-ea34fd9251a2.PNG
   :alt: pyzshcomplete_example


Introduction
============

This project was inspired by `argcomplete <https://github.com/kislyuk/argcomplete>`_, which supplies argument completion for ``bash``.

While having a workaround for ``zsh`` (which just enables compatibility for ``bash`` completion scripts), ``argcomplete`` can't use the full power of the ``zsh`` completion system (e.g. show flag help messages).

``pyzshcomplete`` was written to utilize as many of the features offered by ``zsh`` as possible.


Installation
============

.. code-block:: zsh

    pip install pyzshcomplete
    ~/.local/bin/activate_pyzshcomplete

Restart ``zsh`` after the installation is complete.

**NOTE 1**: The path to ``activate_pyzshcomplete`` will differ depending on where pip installs packages, and it may not be in your ``PATH``, so you will have to find it.

**Note 2**: Removing the package will leave residual files in your system. This is currently unavoidable, since ``pip`` is not aware of these files. For those who want to clean up their system, take a look at the source of ``activate_pyzshcomplete``

Usage
=====

To emphasize the similarity to ``argcomplete``, here is the example usage shown in the ``argcomplete`` readme:

.. code-block:: python

    #!/usr/bin/env python
    # PYTHON_ARGCOMPLETE_OK
    import argcomplete, argparse
    parser = argparse.ArgumentParser()
    ...
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    ...

And here it is adapted to ``pyzshcomplete``:

.. code-block:: python

    #!/usr/bin/env python
    # PYZSHCOMPLETE_OK
    import pyzshcomplete, argparse
    parser = argparse.ArgumentParser()
    ...
    pyzshcomplete.autocomplete(parser)
    args = parser.parse_args()
    ...

Note that the magic string ``PYZSHCOMPLETE_OK`` is required to appear at the top of the script. This is similar to the ``PYTHON_ARGCOMPLETE_OK`` magic of ``argcomplete``.


The ``autocomplete(parser)`` method
-----------------------------------

This method is the interface to the autocompletion mechanism. It **must** be called after the parser construction is complete, but **before** the arguments are parsed.

It receives your parser as an argument, converts it to a ``zsh`` completion script format passes it on and exits the ``python`` program. The output is then used by the ``zsh`` completion system to generate completions.

The consequences are that your program is actually being run as part of argument completion and anything you do prior to calling ``autocomplete`` will happen **every** time the user attempts autocompletion. Additionally, if it takes a long time for the program to reach ``autocomplete``, this time will be reflected as a lag that the user will experience.


Can I use both ``argcomplete`` and ``pyzshcomplete``?
-----------------------------------------------------

TL;DR: **Yes!**

example:

.. code:: python

    #!/usr/bin/env python3
    # PYTHON_ARGCOMPLETE_OK
    # PYZSHCOMPLETE_OK

    from argparse import ArgumentParser
    import pyzshcomplete, argcomplete

    parser = ArgumentParser()
    parser.add_argument('arg')

    # These lines can be in any order
    argcomplete.autocomplete(parser)
    pyzshcomplete.autocomplete(parser)

    args = parser.parse_args()

Both ``argcomplete`` and ``pyzshcomplete`` use an environment variable set by the completion script that is unique to that shell. If that variable is not set, the ``autocomplete`` function simply returns without doing anything.

``argcomplete`` uses ``_ARGCOMPLETE`` and ``pyzshcomplete`` uses ``PYZSHCOMPLETE``. this means that if you're using ``bash``, the ``_ARGCOMPLETE`` environment variable will be set, and only ``argcomplete.autocomplete`` will do completion magic, and vice versa if you're using ``zsh``.

Smart Completion
----------------

``zsh`` offers easy ways to complete things such as process ids, user accounts, network interfaces, bookmarks and more.

As of this moment, there is no mechanism that enables associating an argument with these options. Stay tuned, as it is a prioritized feature.


Supported Parsers
=================

``pyzshcomplete`` was written to be easy to extend for new parsers. It currently supports only ``argparse``, but you are welcome to request or contribute support for other parsers.


Non-Supported Features
======================

Some features of certain parsers can't be (easily enough) supported by ``zsh`` or ``pyzshcomplete`` and are listed here for public knowledge.

General
-------

- Completion for ``python`` modules (``python -m <module>``)

Argparse
--------

-  **Subparsers** - Subparsers **will** be supported in the near future.
-  Custom actions - There is no way to know in advance what effect will actions have on the way the argument should be supplied (e.g. can a flag be specified multiple times?).
-  Non-standard flag prefixes - Only the ``-`` and ``+`` prefixes are supported, as that is what the ``_arguments`` completion utility supports.
-  Usage of the ``from_file_prefix_chars`` in ``ArgumentParser``


Python Support
==============

Official support is for Python 3 only.


Feature Requests and Bug Reports
================================

Feature requests and bug reports are tracked on `Github <https://github.com/dan1994/pyzshcomplete/issues>`_.


Resources
=========

Getting into ``zsh`` internals isn't easy. If you are interested to learn more of the inner workings, take a look at the following resources:

-  From Bash to Z Shell - This book is intended to teach ``zsh`` by example, and is much more easy to read than any manual or user guide I've encountered (You can find the full pdf in a simple search, but I didn't tell you that).
-  `The Zsh Manual <http://zsh.sourceforge.net/Doc/zsh_a4.pdf>`_ - After you've acquainted yourself with the basics, and want the full spec of anything particular, this is the document to go to.
-  `Zsh Reference Card <http://www.bash2zsh.com/zsh_refcard/refcard.pdf>`_ - After you know what you're doing, you can use this reference card for quick reminders.


License
=======

Licensed under the terms of the MIT License.
