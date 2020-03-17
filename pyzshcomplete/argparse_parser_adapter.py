from pyzshcomplete.parser_adapter import ParserAdapter
from pyzshcomplete.argparse_argument_adapter import ArgparseArgumentAdapter


class ArgparseParserAdapter(ParserAdapter):

    def _inspect_parser_arguments(self):
        self._arguments = [ArgparseArgumentAdapter(self, action)
                           for action in self._parser._actions]
