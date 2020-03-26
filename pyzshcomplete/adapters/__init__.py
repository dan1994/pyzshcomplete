'''
This package contains parser adapters. The purpose of the adapters is to create
a unified interface that is easy to work with when generating completion output.
This makes the code that generates completions more readable, and allows to plug
in new parsers easily.

Each supported parser (e.g. argparse) must create a subpackage and subclass the
classes under the base subpackage.

Also, make sure to update the global code that chooses an adapter based on the
parser type.
'''
