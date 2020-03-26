from sys import exit

from pyzshcomplete.adapters.argparse.parser_adapter import ArgparseParserAdapter


class ZshCompleter:

    def __init__(self, parser):
        self._parser = ArgparseParserAdapter(parser)
        self._arguments = str(self._parser)

    def complete(self):
        print(self._arguments)
        self._exit()

    def _exit(self):
        return_code = 0 if len(self._arguments) > 0 else -1
        exit(return_code)
