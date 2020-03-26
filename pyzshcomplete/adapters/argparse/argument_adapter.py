from argparse import _HelpAction, _VersionAction, _AppendAction, \
    _AppendConstAction, _CountAction, OPTIONAL, ZERO_OR_MORE, ONE_OR_MORE, \
    REMAINDER, SUPPRESS
# _ExtendAction was added in python3.8
try:
    from argparse import _ExtendAction
except ImportError:
    _ExtendAction = _AppendAction

from pyzshcomplete.adapters.base.argument_adapter import ArgumentAdapter, \
    ZshConstants


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
        # The 'optionality' of the argument is checked using is_optional
        if self._argument.nargs == OPTIONAL:
            return 1
        # These cases are non-trivial: This function should always return an
        # int, and the cases that denote an unlimited number of arguments are
        # handled by checking is_rest_of_arguments.
        if self._argument.nargs in [ZERO_OR_MORE, ONE_OR_MORE, REMAINDER]:
            return 1
        return self._argument.nargs

    @property
    def help(self):
        if self._argument.help == SUPPRESS:
            return ''
        # TODO - argparse help can have placeholders that it automatically
        # replaces when displaying the help. We should do the same
        return self._argument.help

    @property
    def is_optional(self):
        if self.is_positional:
            # The ZERO_OR_MORE case is handled by is_rest_of_arguments
            return self._argument.nargs == OPTIONAL
        return not self._argument.required

    @property
    def is_exclusive(self):
        return isinstance(self._argument, (_HelpAction, _VersionAction))

    @property
    def can_repeat(self):
        return isinstance(self._argument, (_AppendAction, _AppendConstAction,
                                           _ExtendAction, _CountAction))

    @property
    def is_rest_of_arguments(self):
        return self._argument.nargs in [ZERO_OR_MORE, ONE_OR_MORE, REMAINDER]

    @property
    def complete_with(self):
        if self._argument.choices is not None:
            return ArgumentAdapter.COMPLETE_WITH_CHOICES
        if self._argument.type in (int, float, complex, bool):
            return ZshConstants.DONT_COMPLETE
        return ZshConstants.Tags.FILES

    @property
    def completion_choices(self):
        return self._argument.choices
