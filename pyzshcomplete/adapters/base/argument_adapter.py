from abc import ABCMeta, abstractmethod


class ArgumentAdapter(metaclass=ABCMeta):

    def __init__(self, parser, argument):
        self._parser = parser
        self._argument = argument

    @property
    def is_positional(self):
        return not self.is_optional

    @property
    @abstractmethod
    def is_optional(self):
        return

    @property
    @abstractmethod
    def name(self):
        return

    @property
    @abstractmethod
    def options(self):
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
    @abstractmethod
    def is_exclusive(self):
        return

    @property
    @abstractmethod
    def can_repeat(self):
        return


class StringifyableArgumentAdapter(ArgumentAdapter):

    SUBARGUMENT_LOCATION = '+'

    def __str__(self):
        if self.is_optional:
            return self._optional_argument_to_string()
        return self._positional_argument_to_string()

    def _optional_argument_to_string(self):
        return '{exclusion_list}{options}{subargument_location}{help}' \
            '{subarguments}'.format(
                exclusion_list=self._exclusion_list_to_string(),
                options=self._options_to_string(),
                subargument_location=self._subargument_location_to_string(),
                help=self._help_to_string(),
                subarguments=self._subarguments_to_string()
            )

    def _positional_argument_to_string(self):
        if self.subargument_count != 1:
            raise NotImplementedError(
                'A positional argument can currently be completed only once')

        return ':{message}:{completions}'.format(
            message=self._name_and_help_to_string(),
            completions=self._completions_to_string()
        )

    def _exclusion_list_to_string(self):
        if self.is_exclusive:
            return '(* -)'
        # TODO - Missing exclusion of exclusive options for below cases
        if self.can_repeat:
            return ''
        return '({})'.format(' '.join(self.options))

    def _options_to_string(self):
        return '{{{}}}'.format(','.join(self.options))

    def _subargument_location_to_string(self):
        if self.subargument_count == 1:
            return StringifyableArgumentAdapter.SUBARGUMENT_LOCATION
        return ''

    def _help_to_string(self):
        if len(self.help) > 0:
            return '[{}]'.format(self.help)
        return ''

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
