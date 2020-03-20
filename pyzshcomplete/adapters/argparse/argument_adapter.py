from argparse import _HelpAction, _VersionAction, _AppendAction, \
    _AppendConstAction
# _ExtendAction was added in python3.8
try:
    from argparse import _ExtendAction
except ImportError:
    _ExtendAction = _AppendAction

from pyzshcomplete.adapters.base.argument_adapter import ArgumentAdapter


class ArgparseArgumentAdapter(ArgumentAdapter):

    @property
    def is_flag(self):
        return len(self._argument.option_strings) > 0

    @property
    def name(self):
        if self._argument.metavar is not None:
            return self._argument.metavar
        return self._argument.dest

    @property
    def flags(self):
        if self.is_positional:
            raise TypeError('A positional argument doesn\'t have flags')
        return self._argument.option_strings

    @property
    def subargument_count(self):
        if self._argument.nargs is None:
            return 1
        return self._argument.nargs

    @property
    def help(self):
        return self._argument.help

    @property
    def is_optional(self):
        if self.is_positional:
            return self._argument.nargs in ['?', '*']
        return not self._argument.required

    @property
    def is_exclusive(self):
        return isinstance(self._argument, (_HelpAction, _VersionAction))

    @property
    def can_repeat(self):
        return isinstance(self._argument,
                          (_AppendAction, _AppendConstAction, _ExtendAction))
