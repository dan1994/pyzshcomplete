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

    @property
    @abstractmethod
    def complete_with(self):
        return

    @property
    @abstractmethod
    def completion_choices(self):
        return


class ArgumentAdapter(ArgumentAdapterInterface):

    COMPLETE_WITH_CHOICES = 'choices'

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
        # TODO - Missing exclusion of exclusive options for below cases
        if self.can_repeat:
            return ''
        return '({})'.format(' '.join(self.flags))

    def _can_repeat_to_string(self):
        return ZshConstants.REPEATING_ARGUMENT if self.can_repeat else ''

    def _flags_to_string(self):
        self._validate_flags_prefix()
        return '{{{}}}'.format(','.join(self.flags))

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

    def _is_optional_to_string(self):
        return ZshConstants.OPTIONAL_ARGUMENT if self.is_optional else ''

    def _name_and_help_to_string(self):
        if self.help is not None and len(self.help) > 0:
            return '{} - {}'.format(self.name, self._escaped_help())
        return self.name

    def _escaped_help(self):
        return self.help.replace(r':', r'\:')

    def _subarguments_to_string(self):
        return self.subargument_count * \
            '{}: :{}'.format(
                self._has_variable_subarguments_to_string(),
                self._completions_to_string()
            )

    def _has_variable_subarguments_to_string(self):
        return ZshConstants.VARIABLE_SUBARGUMENTS if self.is_rest_of_arguments \
            else ''

    def _completions_to_string(self):
        if self.complete_with == ArgumentAdapter.COMPLETE_WITH_CHOICES:
            return self._choices_to_string()
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
            return {completion: None for completion in self.completion_choices}
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


class ZshConstants:

    SUPPORTED_PREFIXES = ['+', '-']

    OPTIONAL_ARGUMENT = ':'
    REPEATING_ARGUMENT = '*'
    VARIABLE_SUBARGUMENTS = '*'

    class Exclusion:
        REST_OF_ARGUMENTS = '*'
        POSITIONAL = ':'
        FLAGS = '-'

    class SubargumentSeparator:
        NO_SEPARATOR = '-'
        SPACE = ''
        EQUAL_SIGN = '=-'
        NONE_OR_SPACE = '+'
        EQUAL_SIGN_OR_SPACE = '='

    class Tags:
        ACCOUNTS = 'accounts'
        ALL_EXPANSIONS = 'all-expansions'
        ALL_FILES = 'all-files'
        ARGUMENTS = 'arguments'
        ARRAYS = 'arrays'
        ASSOCIATION_KEYS = 'association-keys'
        BOOKMARKS = 'bookmarks'
        BUILTINS = 'builtins'
        CHARACTERS = 'characters'
        COLORMAPIDS = 'colormapids'
        COLORS = 'colors'
        COMMANDS = 'commands'
        CONTEXTS = 'contexts'
        CORRECTIONS = 'corrections'
        CURSORS = 'cursors'
        DEFAULT = 'default'
        DESCRIPTIONS = 'descriptions'
        DEVICES = 'devices'
        DIRECTORIES = 'directories'
        DIRECTORY_STACK = 'directory-stack'
        DISPLAYS = 'displays'
        DOMAINS = 'domains'
        EXPANSIONS = 'expansions'
        FILE_DESCRIPTORS = 'file-descriptors'
        FILES = 'files'
        FONTS = 'fonts'
        FSTYPES = 'fstypes'
        FUNCTIONS = 'functions'
        GLOBBED_FILES = 'globbed-files'
        GROUPS = 'groups'
        HISTORY_WORDS = 'history-words'
        HOSTS = 'hosts'
        INDEXES = 'indexes'
        JOBS = 'jobs'
        INTERFACES = 'interfaces'
        KEYMAPS = 'keymaps'
        KEYSYMS = 'keysyms'
        LIBRARIES = 'libraries'
        LIMITS = 'limits'
        LOCAL_DIRECTORIES = 'local-directories'
        MANUALS = 'manuals'
        MAILBOXES = 'mailboxes'
        MAPS = 'maps'
        MESSAGES = 'messages'
        MODIFIERS = 'modifiers'
        MODULES = 'modules'
        MY_ACCOUNTS = 'my-accounts'
        NAMED_DIRECTORIES = 'named-directories'
        NAMES = 'names'
        NEWSGROUPS = 'newsgroups'
        NICKNAMES = 'nicknames'
        OPTIONS = 'options'
        ORIGINAL = 'original'
        OTHER_ACCOUNTS = 'other-accounts'
        PACKAGES = 'packages'
        PARAMETERS = 'parameters'
        PATH_DIRECTORIES = 'path-directories'
        PATHS = 'paths'
        PODS = 'pods'
        PORTS = 'ports'
        PREFIXES = 'prefixes'
        PRINTERS = 'printers'
        PROCESSES = 'processes'
        PROCESSES_NAMES = 'processes-names'
        SEQUENCES = 'sequences'
        SESSIONS = 'sessions'
        SIGNALS = 'signals'
        STRINGS = 'strings'
        STYLES = 'styles'
        SUFFIXES = 'suffixes'
        TAGS = 'tags'
        TARGETS = 'targets'
        TIME_ZONES = 'time-zones'
        TYPES = 'types'
        URLS = 'urls'
        USERS = 'users'
        VALUES = 'values'
        VARIANT = 'variant'
        VISUALS = 'visuals'
        WARNINGS = 'warnings'
        WIDGETS = 'widgets'
        WINDOWS = 'windows'
        ZSH_OPTIONS = 'zsh-options'
