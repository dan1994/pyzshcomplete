from pyzshcomplete.meta_argument import MetaArgument


class MetaParser:

    def __init__(self, parser):
        self._parser = parser
        self._meta_arguments = [MetaArgument(action)
                                for action in self._parser._actions]

    @property
    def arguments(self):
        return self._meta_arguments

    @property
    def positional_arguments(self):
        return filter(lambda arg: arg.is_positional(), self._meta_arguments)

    @property
    def optional_arguments(self):
        return filter(lambda arg: arg.is_optional(), self._meta_arguments)
