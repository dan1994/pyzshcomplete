from argparse import _HelpAction, _VersionAction, _AppendAction, _AppendConstAction
try:
    from argparse import _ExtendAction
except ImportError:
    _ExtendAction = _AppendAction

from pyzshcomplete.argument_adapter import StringifyableArgumentAdapter


class ArgparseArgumentAdapter(StringifyableArgumentAdapter):

    def is_optional(self):
        return len(self._argument.option_strings) > 0

    def name(self):
        return self._argument.dest

    def options(self):
        if self.is_positional():
            raise TypeError('A positional argument doesn\'t have options')
        return self._argument.option_strings

    def subargument_count(self):
        if self._argument.nargs is None:
            return 1
        return self._argument.nargs

    def help(self):
        return self._argument.help

    def is_exclusive(self):
        return isinstance(self._argument, (_HelpAction, _VersionAction))

    def can_repeat(self):
        return isinstance(self._argument,
                          (_AppendAction, _AppendConstAction, _ExtendAction))
