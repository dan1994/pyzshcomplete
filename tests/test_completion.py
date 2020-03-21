def test_empty(empty_parser, autocomplete_and_compare):
	autocomplete_and_compare(empty_parser, [''])


def test_default(default_parser, autocomplete_and_compare):
	autocomplete_and_compare(default_parser, [
		r'(* : -){-h,--help}[show this help message and exit]'
	])


def test_positional(empty_parser, autocomplete_and_compare):
	empty_parser.add_argument('pos', help='A positional argument')
	autocomplete_and_compare(
		empty_parser, [r':pos - A positional argument:_default'])


def test_optional(empty_parser, autocomplete_and_compare):
	empty_parser.add_argument('-o', help='An optional argument')
	autocomplete_and_compare(empty_parser, [
		r'(-o){-o}+[An optional argument]: :_default'
	])
