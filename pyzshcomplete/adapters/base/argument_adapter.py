from abc import ABCMeta, abstractmethod


class ArgumentAdapterInterface(metaclass=ABCMeta):

    def __init__(self, parser, argument):
        self._parser = parser
        self._argument = argument

    @property
    def is_positional(self):
        return not self.is_flag

    @property
    @abstractmethod
    def is_flag(self):
        return

    @property
    @abstractmethod
    def name(self):
        return

    @property
    @abstractmethod
    def flags(self):
        return

    @property
    @abstractmethod
    def subargument_count(self):
        return

    @property
    @abstractmethod
    def help(self):
        return

    @property
    def is_required(self):
        return not self.is_optional

    @property
    @abstractmethod
    def is_optional(self):
        return

    @property
    @abstractmethod
    def is_exclusive(self):
        return

    @property
    @abstractmethod
    def can_repeat(self):
        return


class ArgumentAdapter(ArgumentAdapterInterface):

    SUBARGUMENT_SPACE_SEPERATOR = ''
    SUBARGUMENT_NO_SEPARATOR = '-'
    SUBARGUMENT_EITHER_NO_OR_SPACE_SEPARATOR = '+'
    SUBARGUMENT_EITHER_EQUAL_SIGN_OR_SPACE_SEPERATOR = '='
    SUBARGUMENT_EITHER_EQUAL_SIGN_SEPERATOR = '=-'

    def __str__(self):
        if self.is_flag:
            return self._flag_argument_to_string()
        return self._positional_argument_to_string()

    def _flag_argument_to_string(self):
        return '{exclusion_list}{can_repeat}{flags}{subargument_separator}'\
            '{help}{subarguments}'.format(
                exclusion_list=self._exclusion_list_to_string(),
                can_repeat=self._can_repeat_to_string(),
                flags=self._flags_to_string(),
                subargument_separator=self._subargument_separator_to_string(),
                help=self._help_to_string(),
                subarguments=self._subarguments_to_string()
            )

    def _positional_argument_to_string(self):
        if self.subargument_count != 1:
            raise NotImplementedError(
                'A positional argument can currently be completed only once')

        return ':{is_optional}{message}:{completions}'.format(
            is_optional=self._is_optional_to_string(),
            message=self._name_and_help_to_string(),
            completions=self._completions_to_string()
        )

    def _exclusion_list_to_string(self):
        if self.is_exclusive:
            return '(* -)'
        # TODO - Missing exclusion of exclusive options for below cases
        if self.can_repeat:
            return ''
        return '({})'.format(' '.join(self.flags))

    def _can_repeat_to_string(self):
        return '*' if self.can_repeat else ''

    def _flags_to_string(self):
        return '{{{}}}'.format(','.join(self.flags))

    def _subargument_separator_to_string(self):
        if self.subargument_count == 1:
            return ArgumentAdapter.SUBARGUMENT_EITHER_NO_OR_SPACE_SEPARATOR
        return ArgumentAdapter.SUBARGUMENT_SPACE_SEPERATOR

    def _help_to_string(self):
        if len(self.help) > 0:
            return '[{}]'.format(self.help)
        return ''

    def _is_optional_to_string(self):
        return ':' if self.is_optional else ''

    def _name_and_help_to_string(self):
        if len(self.help) > 0:
            return '{} - {}'.format(self.name, self.help)
        return self.name

    def _subarguments_to_string(self):
        return ': :{}'.format(self._completions_to_string()) * \
            self.subargument_count

    def _completions_to_string(self):
        # TODO - Implement more complicated completers such as choice completer
        return '_files'