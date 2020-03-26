#!/usr/bin/python3

from argparse import ArgumentParser
from sys import exit


class ZshCompleter:

	def __init__(self, parser):
		self._parser = parser
		self._arguments = []

	def complete(self):
		self._collect_arguments()
		self._print_arguments()
		self._exit()

	def _collect_arguments(self):
		positional_index = 1
		for action in self._parser._actions:
			if action.option_strings:
				for option in action.option_strings:
					help_string = '[{}]'.format(action.help) if action.help is not None else ''
					if action.nargs == 0:
						self._arguments.append('{}{}'.format(option, help_string))
					else:
						self._arguments.append('{}+{}:{} arg:_files'.format(option, help_string, action.dest))
			else:
				self._arguments.append('{}:{}:_files'.format(positional_index, action.dest))
				positional_index += 1

	def _print_arguments(self):
		for argument in self._arguments:
			print(argument)

	def _exit(self):
		return_code = 0 if len(self._arguments) > 0 else -1
		exit(return_code)
