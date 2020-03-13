from os import environ

from pyzshcomplete.zsh_completer import ZshCompleter


__all__ = ['autocomplete']


def autocomplete(parser):
	if not _running_in_autocompletion_context():
		return

	completer = ZshCompleter(parser)
	completer.complete()


def _running_in_autocompletion_context():
	return 'ARGCOMPLETE' in environ
