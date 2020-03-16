class MetaArgument:

    def __init__(self, argparse_action):
        self._action = argparse_action

    @property
    def name(self):
        return self._action.dest

    @property
    def options(self):
        if self.is_positional:
            raise TypeError('A positional argument doesn\'t have options')
        return self._action.option_strings

    def __len__(self):
        if self._action.nargs is None:
            return 1
        return self._action.nargs

    @property
    def is_positional(self):
        return not self.is_optional

    @property
    def is_optional(self):
        return len(self._action.option_strings) > 0

    @property
    def help(self):
        return self._action.help
