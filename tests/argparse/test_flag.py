def test_default(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('-o')
    autocomplete_and_compare(empty_parser, [
        r'(-o){-o}+: :_default'
    ])
