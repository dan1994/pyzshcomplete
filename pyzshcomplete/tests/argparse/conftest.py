from pytest import fixture
from argparse import ArgumentParser


@fixture(scope='function')
def default_parser():
    return ArgumentParser(prog='program')


@fixture(scope='function')
def empty_parser():
    return ArgumentParser(prog='program', add_help=False)
