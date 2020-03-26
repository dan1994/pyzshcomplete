from argparse import OPTIONAL, ZERO_OR_MORE, REMAINDER


def test_cat(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('-A', '--show-all', action='store_true',
                              help='equivalent to -vET')
    empty_parser.add_argument('-b', '--number-nonblank', action='store_true',
                              help='number nonempty output lines, overrides -n')
    empty_parser.add_argument('-e', action='store_true',
                              help='equivalent to -vE')
    empty_parser.add_argument('-E', '--show-ends', action='store_true',
                              help='display $ at end of each line')
    empty_parser.add_argument('-n', '--number', action='store_true',
                              help='number all output lines')
    empty_parser.add_argument('-s', '--squeeze-blank', action='store_true',
                              help='suppress repeated empty output lines')
    empty_parser.add_argument('-t', action='store_true',
                              help='equivalent to -vT')
    empty_parser.add_argument('-T', '--show-tabs', action='store_true',
                              help='display TAB characters as ^I')
    empty_parser.add_argument('-u', action='store_true', help='ignored')
    empty_parser.add_argument('-v', '--show-nonprinting', action='store_true',
                              help='use ^ and M- notation, except for LFD and '
                              'TAB')
    empty_parser.add_argument('--help', action='help',
                              help='display help and exit')
    empty_parser.add_argument('--version', action='version',
                              help='output version information and exit')
    empty_parser.add_argument('files', nargs=ZERO_OR_MORE)

    autocomplete_and_compare(empty_parser, [
        r'(-A --show-all){-A,--show-all}[equivalent to -vET]',
        r'(-b --number-nonblank){-b,--number-nonblank}[number nonempty output lines, overrides -n]',
        r'(-e){-e}[equivalent to -vE]',
        r'(-E --show-ends){-E,--show-ends}[display $ at end of each line]',
        r'(-n --number){-n,--number}[number all output lines]',
        r'(-s --squeeze-blank){-s,--squeeze-blank}[suppress repeated empty output lines]',
        r'(-t){-t}[equivalent to -vT]',
        r'(-T --show-tabs){-T,--show-tabs}[display TAB characters as ^I]',
        r'(-u){-u}[ignored]',
        r'(-v --show-nonprinting){-v,--show-nonprinting}[use ^ and M- notation, except for LFD and TAB]',
        r'(* : -){--help}[display help and exit]',
        r'(* : -){--version}[output version information and exit]',
        r'*:files:_files'
    ])


def test_ps(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('-a', action='store_true', help='select processes '
                              'with tty except session leaders')
    empty_parser.add_argument('-A', '-e', action='store_true',
                              help='select every process')
    empty_parser.add_argument('-d', action='store_true', help='select all '
                              'processes except session leaders')
    empty_parser.add_argument('-p', action='append', type=int,
                              help='select processes by ID')
    empty_parser.add_argument('-G', action='append',
                              help='select processes by real group')
    empty_parser.add_argument('-g', action='append', help='select processes by '
                              'effective group or session')
    empty_parser.add_argument('-s', action='append', type=int,
                              help='select processes by session leaders')
    empty_parser.add_argument('-t', action='append',
                              help='select processes by attached terminal')
    empty_parser.add_argument('-u', action='append',
                              help='select processes by effective user')
    empty_parser.add_argument('-U', action='append',
                              help='select processes by real user')
    empty_parser.add_argument('-o', help='specify output format')
    empty_parser.add_argument('-c', action='store_true',
                              help='show scheduler properties')
    empty_parser.add_argument('-f', action='store_true',
                              help='full listing')
    empty_parser.add_argument('-j', action='store_true',
                              help='show session ID and process group ID')
    empty_parser.add_argument('-l', action='store_true',
                              help='long listing')
    empty_parser.add_argument('-L', action='store_true', help='show '
                              'information about each light weight process')
    empty_parser.add_argument('-y', action='store_true',
                              help='show RSS in place of ADDR (used with -l)')
    empty_parser.add_argument('--help', nargs=OPTIONAL,
                              choices=['simple', 'list', 'output',
                                       'threads', 'misc', 'all'],
                              help='display help information')
    empty_parser.add_argument('--info', action='help',
                              help='display debugging information')
    empty_parser.add_argument('-V', '--version', action='version',
                              help='display version information')

    autocomplete_and_compare(empty_parser, [
        r'(-a){-a}[select processes with tty except session leaders]',
        r'(-A -e){-A,-e}[select every process]',
        r'(-d){-d}[select all processes except session leaders]',
        r'*{-p}+[select processes by ID]: : ',
        r'*{-G}+[select processes by real group]: :_files',
        r'*{-g}+[select processes by effective group or session]: :_files',
        r'*{-s}+[select processes by session leaders]: : ',
        r'*{-t}+[select processes by attached terminal]: :_files',
        r'*{-u}+[select processes by effective user]: :_files',
        r'*{-U}+[select processes by real user]: :_files',
        r'(-o){-o}+[specify output format]: :_files',
        r'(-c){-c}[show scheduler properties]',
        r'(-f){-f}[full listing]',
        r'(-j){-j}[show session ID and process group ID]',
        r'(-l){-l}[long listing]',
        r'(-L){-L}[show information about each light weight process]',
        r'(-y){-y}[show RSS in place of ADDR (used with -l)]',
        r'(--help){--help}+[display help information]:: :(simple list output threads misc all)',
        r'(* : -){--info}[display debugging information]',
        r'(* : -){-V,--version}[display version information]'
    ])


def test_ln(empty_parser, autocomplete_and_compare):
    empty_parser.add_argument('-b', action='store_true',
                              help='create a backup of each existing '
                              'destination file')
    empty_parser.add_argument('--backup', nargs=OPTIONAL,
                              choices=['none', 'off', 'numbered', 't',
                                       'existing', 'nil', 'simple', 'never'],
                              help='create a backup of each existing '
                              'destination file')
    empty_parser.add_argument('-d', '-F', '--directory', action='store_true',
                              help='allow the superuser to attempt to hard '
                              'link directories')
    empty_parser.add_argument('-f', '--force', action='store_true',
                              help='remove existing destination files')
    empty_parser.add_argument('-i', '--interactive', action='store_true',
                              help='prompt before removing destination files')
    empty_parser.add_argument('-L', '--logical', action='store_true',
                              help='create hard links to symbolic link '
                              'references')
    empty_parser.add_argument('-n', '--no-dereference', action='store_true',
                              help='treat destination symbolic link to a '
                              'directory as if it were a normal file')
    empty_parser.add_argument('-P', '--physical', action='store_true',
                              help='create hard links directly to symbolic '
                              'links')
    empty_parser.add_argument('-r', '--relative', action='store_true',
                              help='create symbolic links relative to link '
                              'location')
    empty_parser.add_argument('-s', '--symbolic', action='store_true',
                              help='create symbolic links instead of hard '
                              'links')
    empty_parser.add_argument('-S', '--suffix',
                              help='override default backup suffix')
    empty_parser.add_argument('-t', '--target-directory',
                              dest='target_directory',
                              help='specify directory in which to create the '
                              'links')
    empty_parser.add_argument('-T', '--no-target-directory',
                              action='store_const', const='',
                              dest='target_directory',
                              help='treat destination as a normal file')
    empty_parser.add_argument('-v', '--verbose', action='store_true',
                              help='print name of each linked file')
    empty_parser.add_argument('--help', action='help',
                              help='display usage information and exit')
    empty_parser.add_argument('--version', action='version',
                              help='display version information and exit')
    empty_parser.add_argument('link_target')
    empty_parser.add_argument(' ', nargs=REMAINDER)

    autocomplete_and_compare(empty_parser, [
        r'(-b){-b}[create a backup of each existing destination file]',
        r'(--backup){--backup}+[create a backup of each existing destination file]:: :(none off numbered t existing nil simple never)',
        r'(-d -F --directory){-d,-F,--directory}[allow the superuser to attempt to hard link directories]',
        r'(-f --force){-f,--force}[remove existing destination files]',
        r'(-i --interactive){-i,--interactive}[prompt before removing destination files]',
        r'(-L --logical){-L,--logical}[create hard links to symbolic link references]',
        r'(-n --no-dereference){-n,--no-dereference}[treat destination symbolic link to a directory as if it were a normal file]',
        r'(-P --physical){-P,--physical}[create hard links directly to symbolic links]',
        r'(-r --relative){-r,--relative}[create symbolic links relative to link location]',
        r'(-s --symbolic){-s,--symbolic}[create symbolic links instead of hard links]',
        r'(-S --suffix){-S,--suffix}+[override default backup suffix]: :_files',
        r'(-t --target-directory){-t,--target-directory}+[specify directory in which to create the links]: :_files',
        r'(-T --no-target-directory){-T,--no-target-directory}[treat destination as a normal file]',
        r'(-v --verbose){-v,--verbose}[print name of each linked file]',
        r'(* : -){--help}[display usage information and exit]',
        r'(* : -){--version}[display version information and exit]',
        r':link_target:_files',
        r'*: :_files'
    ])
