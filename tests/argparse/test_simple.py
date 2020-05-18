def test_empty(empty_parser, autocomplete_and_compare):
    autocomplete_and_compare(empty_parser, [''])


def test_default(default_parser, autocomplete_and_compare):
    autocomplete_and_compare(default_parser, [
        r'(* : -){-h,--help}[show this help message and exit]'
    ])
