# -*- coding: utf-8 -*-

from nose.tools.trivial import assert_true, assert_equals

from . import _schema


def test_constant():
	s = _schema()
	s.some_cst_value.constant('blue apple')

	s.validate({'some_cst_value': 'Roger that'})
	assert_true(s.valid)

	assert_equals(s.some_cst_value.result, 'blue apple')