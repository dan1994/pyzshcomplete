from pyzshcomplete.adapters.base.parser_adapter import ParserAdapter
from pyzshcomplete.adapters.argparse.argument_adapter import \
    ArgparseArgumentAdapter


class ArgparseParserAdapter(ParserAdapter):

    def _inspect_parser_arguments(self):
        for argument in self._parser._actions:
            argument_adapter = ArgparseArgumentAdapter(self._parser, argument)
            resulting_arguments = str(argument_adapter).split('\n')
            self._arguments.extend(resulting_arguments)
