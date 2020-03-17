from abc import ABCMeta, abstractmethod


class ParserAdapter(metaclass=ABCMeta):

    def __init__(self, parser):
        self._parser = parser
        self._arguments = []
        self._inspect_parser_arguments()

    def __str__(self):
        return '\n'.join([str(argument) for argument in self._arguments])

    @abstractmethod
    def _inspect_parser_arguments(self):
        return
