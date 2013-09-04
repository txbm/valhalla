import re
from collections import namedtuple

from .. import ValidationError

_regexes = {
	'plain_text': re.compile(r'[\w\W\s]*', re.IGNORECASE),
	'text_to_slug': re.compile(r'\W', re.IGNORECASE),
	'punctuation': re.compile(r'[^\s\w\-]+', re.IGNORECASE),
	'alphanumeric': re.compile(r'[a-z\s\-_0-9]*', re.IGNORECASE),
	'alpha': re.compile(r'[a-z\s\-_]*', re.IGNORECASE),
	'numeric': re.compile(r'\d*', re.IGNORECASE),
	'dash_under_space': re.compile (r'[\-_\s]+', re.IGNORECASE)
}

_disable_prehook = []

def _prehook(*args, **kwargs):
	value = kwargs.get('_value')
	if type(value) is str:
		return unicode(value)
	return value

def text(*args, **kwargs):
	value = kwargs.get('_value')

	if type(value) not in (unicode, str):
		raise ValidationError('Text must be string or unicode type.')

	min_len = kwargs.get('min_len')
	if min_len and len(value) < min_len:
		raise ValidationError('Text length must be greater than %s' % min_len)

	max_len = kwargs.get('max_len')
	if max_len and len(value) > max_len:
		raise ValidationError('Text length must be less than %s' % max_len)

	return value
