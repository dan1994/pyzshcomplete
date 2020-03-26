from abc import ABCMeta, abstractmethod
from sys import stderr


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

    @property
    @abstractmethod
    def is_rest_of_arguments(self):
        return


class ArgumentAdapter(ArgumentAdapterInterface):

    SUBARGUMENT_SPACE_SEPERATOR = ''
    SUBARGUMENT_NO_SEPARATOR = '-'
    SUBARGUMENT_EITHER_NO_OR_SPACE_SEPARATOR = '+'
    SUBARGUMENT_EITHER_EQUAL_SIGN_OR_SPACE_SEPERATOR = '='
    SUBARGUMENT_EITHER_EQUAL_SIGN_SEPERATOR = '=-'

    def __str__(self):
        try:
            if self.is_flag:
                return self._flag_argument_to_string()
            return self._positional_argument_to_string()
        except Exception as e:
            stderr.write('Skipping argument due to an exception: {}'.format(e))
            return ''

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
        message = self._name_and_help_to_string()
        completions = self._completions_to_string()

        if self.is_rest_of_arguments:
            return '*:{message}:{action}'.format(
                message=message,
                action=completions
            )

        return self.subargument_count * \
            ':{is_optional}{message}:{action}'.format(
                is_optional=self._is_optional_to_string(),
                message=message,
                action=completions
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
        self._validate_flags_prefix()
        return '{{{}}}'.format(','.join(self.flags))

    def _validate_flags_prefix(self):
        prefixes = map(lambda flag: flag[0], self.flags)
        bad_prefixes = list(
            filter(lambda prefix: prefix not in ['-', '+'], prefixes))

        if len(bad_prefixes) > 0:
            raise ValueError('Flag uses the {} prefix that is not supported by '
                             'zsh. Only - and + are supported as flag prefixes'
                             .format(bad_prefixes[0]))

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
        return self.subargument_count * \
            '{}: :{}'.format(
                self._has_variable_subarguments_to_string(),
                self._completions_to_string()
            )

    def _completions_to_string(self):
        # TODO - Implement more complicated completers such as choice completer
        return '_files'

    def _has_variable_subarguments_to_string(self):
        return '*' if self.is_rest_of_arguments else ''
