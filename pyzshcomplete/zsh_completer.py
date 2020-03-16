from sys import exit

from pyzshcomplete.meta_parser import MetaParser


class ZshCompleter:

    def __init__(self, parser):
        self._parser = MetaParser(parser)
        self._arguments = []

    def complete(self):
        self._collect_arguments()
        self._print_arguments()
        self._exit()

    def _collect_arguments(self):
        positional_index = 1
        for argument in self._parser.arguments:
            if argument.is_optional:
                for option in argument.options:
                    help_string = '[{}]'.format(
                        argument.help) if argument.help is not None else ''
                    if len(argument) == 0:
                        self._arguments.append(
                            '{}{}'.format(option, help_string))
                    else:
                        self._arguments.append(
                            '{}+{}:{} arg:_files'.format(option,
                                                         help_string,
                                                         argument.name))
            else:
                self._arguments.append('{}:{}:_files'.format(
                    positional_index, argument.name))
                positional_index += 1

    def _print_arguments(self):
        for argument in self._arguments:
            print(argument)

    def _exit(self):
        return_code = 0 if len(self._arguments) > 0 else -1
        exit(return_code)
