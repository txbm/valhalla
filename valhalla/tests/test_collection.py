from nose.tools.trivial import assert_equals, assert_true, assert_false, assert_is, assert_is_instance

from .. import Schema

test_data = {
	'some_dict': {'one': 'fish', 'two': 'fish', 'red': 'fish', 'blue': 'fish'},
	'some_list': ['alpha', 'bravo', 'charlie', 'delta']
}

def _schema():
	return Schema('Test Schema')

def test_drop_keys():
	s = _schema()
	s.some_dict.drop_keys(('one', 'two'))

	s.validate(test_data)
	assert_true(s.valid)

	assert_equals(s.some_dict.result, {'red': 'fish', 'blue': 'fish'})

def test_contains():
	s = _schema()
	s.some_list.contains('bravo')

	s.validate(test_data)
	assert_true(s.valid)
