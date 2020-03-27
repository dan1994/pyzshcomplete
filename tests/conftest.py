from pytest import fixture

from pyzshcomplete import _autocomplete


@fixture(scope='function')
def autocomplete_and_compare():
    def _autocomplete_and_compare(parser, expected):
        actual = _autocomplete(parser).split('\n')
        assert actual == expected

    return _autocomplete_and_compare
