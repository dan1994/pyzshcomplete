from pytest import fixture, raises
from argparse import ArgumentParser
from io import StringIO
import os
import sys

sys.path.append('../pyzshcomplete')
from pyzshcomplete import autocomplete

os.environ['ARGCOMPLETE'] = '1'


@fixture(scope='function')
def output():
	original_stdout = sys.stdout
	sys.stdout = _output = StringIO()
	yield _output
	sys.stdout = original_stdout


@fixture(scope='function')
def default_parser():
	return ArgumentParser()


@fixture(scope='function')
def empty_parser():
	return ArgumentParser(add_help=False)


@fixture(scope='session')
def autocomplete_and_compare():
	def _autocomplete_and_compare(parser, expected):
		with raises(SystemExit):
			autocomplete(parser)
		options = sys.stdout.getvalue().split('\n')[:-1]
		assert sorted(options) == sorted(expected)

	return _autocomplete_and_compare
