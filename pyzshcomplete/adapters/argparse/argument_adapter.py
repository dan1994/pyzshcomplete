from argparse import _HelpAction, _VersionAction, _AppendAction, \
    _AppendConstAction, _CountAction, OPTIONAL, ZERO_OR_MORE, ONE_OR_MORE, \
    REMAINDER, SUPPRESS

# _ExtendAction was added in python3.8
try:
    from argparse import _ExtendAction
except ImportError:
    _ExtendAction = _AppendAction

from pyzshcomplete.adapters.base.argument_adapter import ArgumentAdapter
from pyzshcomplete.utils.zsh_constants import ZshConstants


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
        # handled by checking has_variable_subarguments.
        if self._argument.nargs in [ZERO_OR_MORE, ONE_OR_MORE, REMAINDER]:
            return 1
        return self._argument.nargs

    @property
    def help(self):
        if self._argument.help in (None, SUPPRESS):
            return ''

        return self._argument.help % self._help_format_dict()

    def _help_format_dict(self):
        argument_members_dict = dict()
        for member in ['nargs', 'const', 'default', 'type', 'choices', 'required', 'metavar', 'dest', 'help']:
            argument_members_dict[member] = eval(
                'self._argument.{}'.format(member))

        parser_members_dict = {
            'prog': self._parser.prog
        }

        format_dict = {**parser_members_dict, **argument_members_dict}

        return format_dict

    @property
    def is_optional(self):
        if self.is_positional:
            # The ZERO_OR_MORE case is handled by has_variable_subarguments
            return self._argument.nargs == OPTIONAL
        return not self._argument.required

    @property
    def is_exclusive(self):
        return isinstance(self._argument, (_HelpAction, _VersionAction))

    @property
    def exclusion_list(self):
        exclusions = set()
        for group in self._parser._mutually_exclusive_groups:
            if self._argument in group._group_actions:
                exclusions |= self._group_exclusions(group)
        exclusions -= set(self.flags)
        return list(exclusions)

    @property
    def can_repeat(self):
        return isinstance(self._argument, (_AppendAction, _AppendConstAction,
                                           _ExtendAction, _CountAction))

    @property
    def has_variable_subarguments(self):
        return self._argument.nargs in [ZERO_OR_MORE, ONE_OR_MORE, REMAINDER]

    @property
    def is_subargument_optional(self):
        return self._argument.nargs == OPTIONAL

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

    def _group_exclusions(self, group):
        exclusions = set()
        for action in group._group_actions:
            for flag in action.option_strings:
                exclusions |= set([flag])
        return exclusions
