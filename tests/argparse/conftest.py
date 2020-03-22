from pytest import fixture
from argparse import ArgumentParser


@fixture(scope='function')
def default_parser():
    return ArgumentParser()


@fixture(scope='function')
def empty_parser():
    return ArgumentParser(add_help=False)
