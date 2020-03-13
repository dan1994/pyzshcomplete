def test_empty(output, empty_parser, autocomplete_and_compare):
	autocomplete_and_compare(empty_parser, [])


def test_default(output, default_parser, autocomplete_and_compare):
	autocomplete_and_compare(default_parser, [
		'-h[show this help message and exit]',
		'--help[show this help message and exit]'
	])


def test_positional(output, empty_parser, autocomplete_and_compare):
	empty_parser.add_argument('pos', help='A positional argument')
	autocomplete_and_compare(empty_parser, ['1:pos:_files'])


def test_optional(output, empty_parser, autocomplete_and_compare):
	empty_parser.add_argument('-o', help='An optional argument')
	autocomplete_and_compare(empty_parser, [
		'-o+[An optional argument]:o arg:_files'
	])
