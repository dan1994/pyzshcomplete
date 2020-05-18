from abc import ABCMeta, abstractmethod


class ParserAdapterInterface(metaclass=ABCMeta):
    '''
    DO NOT subclass from this class directly, as it doesn't contain the
    completion generation logic. See ParserAdapter.

    Defines the interface to be implemented by parser adapters.
    '''

    def __init__(self, parser):
        self._parser = parser
        self._arguments = []

    @abstractmethod
    def _inspect_parser_arguments(self):
        '''
        Sets the _arguments member to a list containing one entry per zsh
        argument specification.
        '''

        return


class ParserAdapter(ParserAdapterInterface):
    '''
    ParserAdapter is a wrapper to a parser object (e.g.
    argparse.ArgumentParser). It relies on the interface defined by
    ParserAdapterInterface to create the completion generation logic relevant to
    zsh.

    It cannot be used on its own, since it relies on an unimplemented interface.
    In order to use it, subclass it and implement the interface.
    '''

    def __init__(self, parser):
        super(ParserAdapter, self).__init__(parser)
        self._inspect_parser_arguments()

    def __str__(self):
        return '\n'.join([str(argument) for argument in self._arguments])
