from abc import ABCMeta, abstractmethod

from pyzshcomplete.utils.zsh_constants import ZshConstants


class ArgumentAdapterInterface(metaclass=ABCMeta):
    '''
    DO NOT subclass from this class directly, as it doesn't contain the
    completion generation logic. See ArgumentAdapter.

    Defines the interface to be implemented by argument adapters.
    '''

    def __init__(self, parser, argument):
        self._parser = parser
        self._argument = argument

    @property
    def is_positional(self):
        '''True iff the argument is positional (not a flag).'''
        return not self.is_flag

    @property
    @abstractmethod
    def is_flag(self):
        '''True iff the argument is a flag.'''
        return

    @property
    @abstractmethod
    def name(self):
        '''A string representing the name of the argument (e.g. 'foo').'''
        return

    @property
    @abstractmethod
    def flags(self):
        '''
        If the argument is a flag, returns a list of the flags (e.g.
        ['-f', '--foo']), otherwise the behavior is undefined.
        '''
        return

    @property
    @abstractmethod
    def subargument_count(self):
        '''
        An int indicating how many subarguments does this argument have.

        There are other functions that handle optional or variable arguments.
        '''
        return

    @property
    @abstractmethod
    def help(self):
        '''
        A string representing the help message. If there is no help, return
        an empty string.
        '''
        return

    @property
    def is_required(self):
        '''True iff the argument is required.'''
        return not self.is_optional

    @property
    @abstractmethod
    def is_optional(self):
        '''True iff the argument is not required.'''
        return

    @property
    @abstractmethod
    def is_exclusive(self):
        '''
        True iff this argument should prevent completion of other arguments
        and should not be completed if other arguments have already been
        completed (e.g. '--version').
        '''
        return

    @property
    @abstractmethod
    def exclusion_list(self):
        '''A list of other option flags that cannot be used with this flag'''
        return

    @property
    @abstractmethod
    def can_repeat(self):
        '''
        True if the argument can be supplied multiple times
        (e.g. '-x 1 -x 2').
        '''
        return

    @property
    @abstractmethod
    def has_variable_subarguments(self):
        '''True iff the number of subarguments is not a definitive number.'''
        return

    @property
    def is_subargument_required(self):
        '''True iff the subargument(s) to a given argument is/are required.'''
        return not self.is_subargument_optional

    @property
    @abstractmethod
    def is_subargument_optional(self):
        '''
        True iff the subargument(s) to a given argument is/are not required.
        '''
        return

    @property
    @abstractmethod
    def complete_with(self):
        '''
        Returns what kind of completion this argument should have.

        Return ArgumentAdapter.COMPLETE_WITH_CHOICES if the choices should come
        from a predefined list.

        Return ZshConstants.DO_NOT_COMPLETE if the argument should not be
        completed.

        Otherwise return an item or a list of items from ZshConstants.Tags.
        '''
        return

    @property
    @abstractmethod
    def completion_choices(self):
        '''
        Returns choices for completion. Note that this function will be used
        only if self.complete_with returned with
        ArgumentAdapter.COMPLETE_WITH_CHOICES.

        You may return an item, a list, or a dictionary. If a dictionary is
        given, the keys will be used as completion candidates, and the values
        will be used as help messages to the corresponding candidates.
        '''
        return


class ArgumentAdapter(ArgumentAdapterInterface):
    '''
    ArgumentAdapter is a wrapper to an argument object (e.g. argparse.Action).
    It relies on the interface defined by ArgumentAdapterInterface, to create
    the completion generation logic relevant to zsh.

    It cannot be used on its own, since it relies on an unimplemented interface.
    In order to use it, subclass it and implement the interface.
    '''

    COMPLETE_WITH_CHOICES = 'choices'

    def __str__(self):
        try:
            if self.is_flag:
                return self._flag_argument_to_string()
            return self._positional_argument_to_string()
        except:
            # Skip the argument without stopping the entire autocompletion
            return ''

    def _flag_argument_to_string(self):
        return '\n'.join([
            '{exclusion_list}{can_repeat}{flag}{subargument_separator}'
            '{help}{subarguments}'.format(
                exclusion_list=self._exclusion_list_to_string(),
                can_repeat=self._can_repeat_to_string(),
                flag=flag,
                subargument_separator=self._subargument_separator_to_string(),
                help=self._help_to_string(),
                subarguments=self._subarguments_to_string()
            ) for flag in list(self.flags)])

    def _positional_argument_to_string(self):
        message = self._name_and_help_to_string()
        completions = self._completions_to_string()

        if self.has_variable_subarguments:
            return '{variable_subarguments}:{message}:{action}'.format(
                variable_subarguments=ZshConstants.VARIABLE_SUBARGUMENTS,
                message=message,
                action=completions
            )

        return '\n'.join([
            ':{is_optional}{message}:{action}'.format(
                is_optional=self._is_optional_to_string(),
                message=message,
                action=completions
            )
            for _ in range(self.subargument_count)])

    def _exclusion_list_to_string(self):
        if self.is_exclusive:
            all_exclusions = '{} {} {}'.format(
                ZshConstants.Exclusion.REST_OF_ARGUMENTS,
                ZshConstants.Exclusion.POSITIONAL,
                ZshConstants.Exclusion.FLAGS
            )
            return '({})'.format(all_exclusions)

        exclusion_list = self.exclusion_list
        if not self.can_repeat:
            exclusion_list = self.flags + exclusion_list

        if len(exclusion_list) == 0:
            return ''
        return '({})'.format(' '.join(exclusion_list))

    def _can_repeat_to_string(self):
        return ZshConstants.REPEATING_ARGUMENT if self.can_repeat else ''

    def _validate_flags_prefix(self):
        prefixes = map(lambda flag: flag[0], self.flags)
        bad_prefixes = list(
            filter(lambda prefix: prefix not in ZshConstants.SUPPORTED_PREFIXES,
                   prefixes))

        if len(bad_prefixes) > 0:
            raise ValueError('Flag uses the {} prefix that is not supported by '
                             'zsh. Only - and + are supported as flag prefixes'
                             .format(bad_prefixes[0]))

    def _subargument_separator_to_string(self):
        if self.subargument_count == 1:
            return ZshConstants.SubargumentSeparator.NONE_OR_SPACE
        return ZshConstants.SubargumentSeparator.SPACE

    def _help_to_string(self):
        if self.help is not None and len(self.help) > 0:
            return '[{}]'.format(self._escaped_help())
        return ''

    def _name_and_help_to_string(self):
        if self.help is not None and len(self.help) > 0:
            return '{} - {}'.format(self.name, self._escaped_help())
        return self.name

    def _escaped_help(self):
        return self.help.replace(r':', r'\:').replace('\n', ' ')

    def _is_optional_to_string(self):
        return ZshConstants.OPTIONAL_ARGUMENT if self.is_optional else ''

    def _subarguments_to_string(self):
        completions = self._completions_to_string()
        if self.has_variable_subarguments:
            return ':*: :{}'.format(completions)

        return self.subargument_count * \
            ':{is_optional} :{completions}'.format(
                is_optional=self._is_subargument_optional_to_string(),
                completions=completions
            )

    def _is_subargument_optional_to_string(self):
        return ZshConstants.OPTIONAL_ARGUMENT if self.is_subargument_optional \
            else ''

    def _completions_to_string(self):
        if self.complete_with == ArgumentAdapter.COMPLETE_WITH_CHOICES:
            return self._choices_to_string()
        if self.complete_with == ZshConstants.DONT_COMPLETE:
            return ZshConstants.DONT_COMPLETE
        return self._zsh_tags_to_string()

    def _choices_to_string(self):
        completion_choices = self._choices_to_dict()
        completion_choices_as_string = ' '.join([
            ArgumentAdapter._choice_to_string(choice, description)
            for choice, description in completion_choices.items()])
        return '({})'.format(completion_choices_as_string)

    def _choices_to_dict(self):
        if isinstance(self.completion_choices, dict):
            return self.completion_choices
        if isinstance(self.completion_choices, (list, tuple, set)):
            return {completion: None for completion in
                    list(self.completion_choices)}
        return {self.completion_choices: None}

    @staticmethod
    def _choice_to_string(choice, description):
        if description is None:
            choice_as_string = str(choice)
        else:
            choice_as_string = '{}:{}'.format(choice, description)

        escaped_choice_as_string = choice_as_string.replace(
            ':', r'\:').replace(' ', r'\ ')

        return escaped_choice_as_string

    def _zsh_tags_to_string(self):
        complete_with = self.complete_with
        if not isinstance(self.complete_with, (list, tuple, set)):
            complete_with = [complete_with]

        complete_with = map(lambda tag: '_{}'.format(tag), complete_with)
        return ' '.join(complete_with)
