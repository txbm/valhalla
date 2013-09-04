from nose.tools.trivial import assert_equals, assert_true, assert_false, assert_in

from .. import Schema, Field

def test_schema():
	s = Schema()
	assert_equals(s._fields, {})
	f = s.add_field('test_field', Field(s))
	assert_equals(f, s.test_field)
	d = {'test_field': 'test_value'}
	s.validate(d)
	assert_true(s.valid)
	s.reset()
	assert_false(s.valid)
	s.second_field(alt='other_name', req=True)
	d['other_name'] = 'Test Value A'
	d['second_field'] = 'Test Value B'
	s.validate(d)
	assert_true(s.valid)
	assert_equals(s.other_name.result[0], 'Test Value A')
	assert_equals(s.second_field.result[0], 'Test Value A') # because this should not have been run twice
	s.reset()
	assert_false(s.valid)
	d = {'total_fail': 'will not work'}
	s.validate(d)
	assert_false(s.valid)
	assert_false(s.other_name.valid)
	assert_false(s.second_field.valid)
	assert_true(s.test_field.valid)
	assert_in('This field is required.', s.other_name.errors)