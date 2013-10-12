# -*- coding: utf-8 -*-

from functools import partial
from inspect import getmembers

from filters import lookup

class ValidationError(Exception): pass

from filters.casting import none

class Schema(object):

	def __init__(self, name, match=[], require=[], blank=[], extra='ignore'):
		self._name = name
		self._fields = {}
		self._valid = False
		self._extra = extra
		self._missing = []

		self._field_options = {}
		self._field_options['match'] = match
		self._field_options['require'] = require
		self._field_options['blank'] = blank

	def __getattr__(self, attr):
		return self.add_field(attr, Field(self, attr))

	def __repr__(self):
		return '[Schema: %r] - [%r]' % (self.name, ', '.join([f for f in self._fields]))

	@property
	def name(self):
		return self._name

	@property
	def valid(self):
		return self._valid

	@property
	def missing(self):
		return list(self._missing)

	def add_field(self, name, field):
		self._fields[name] = field
		setattr(self, name, field)
		return field

	def validate(self, data_dict, **kwargs):
		self._valid = True

		self._process_required(data_dict)
		self._process_matching(data_dict)
		self._set_blanks()
		
		for name, field in self._fields.iteritems():
			if not field.validate(data_dict.get(name)):
				self._valid = False

	# options are ['all', None, [], ['fields']]
	def _process_required(self, data_dict):
		if not self._field_options['require']:
			return
		
		if self._field_options['require'] == 'all':
			self._field_options['require'] = self._fields.keys()
		
		for f_name in self._field_options['require']:
			try:
				field = self._fields[f_name]
				field.require()
			except KeyError: pass

		required_fields = set([f.name for f in self._fields if f.required])
		supplied_fields = set(data_dict.keys())

		missing_fields = required_fields - supplied_fields
		for f_name in missing_fields:
			field = self._fields[f_name]
			field._valid = False
			field._errors.append('This field cannot be missing.')

	def _process_matching(self, data_dict):
		if not self._field_options['match']:
			return

		for f_names in self._field_options['match']:
			fields = _names_to_fields(f_names)
			if not all(f.result == fields[0].result for f in fields):
				self._valid = False
				self._errors.append('Fields [%s] do not match.' % ' '.join(f_names))

	def _set_blanks(self):
		if not self._field_options['blank']:
			return

		[f.blank(False) for f in self._fields if f.name not in self._field_options['blank']]

	def _names_to_fields(field_names):
		fields = []
		for f_name in field_names:
			try:
				fields.append(self._fields[f_name])
			except KeyError: pass
		return fields


	def reset(self):
		[f.reset() for n, f in self._fields.iteritems()]
		self._valid = False
		
class Field(object):

	def __init__(self, schema, name):
		self._schema = schema
		self._name = name
		self._filters = []
		self._required = None
		self._blank = None
		self._alternate_name = None
		self._match = None

		self.reset()


	def __repr__(self):
		return '[Field: %r] - [%r, %r, %r] - %r' % (self.name, self._original_value, self._value, self._valid, self._errors)

	@property
	def name(self):
		return self._name

	@property
	def valid(self):
		return self._valid

	@property
	def errors(self):
		return self._errors

	@property
	def original(self):
		return self._original_value

	@property
	def result(self):
		return self._value

	@property
	def required(self):
		if self._required is None:
			return False
		return self._required

	@property
	def blank_allowed(self):
		if self._blank is None:
			return True
		return self._blank

	def reset(self):
		self._ran = False
		self._valid = False
		self._errors = []
		self._original_value = self._value = None

	def validate(self, value):
		if self._ran:
			return self._valid

		self._original_value = self._value = none(_value=value)

		if not self.blank_allowed and self._value is None:
			self._valid = False
			self._errors.append('This field cannot be blank.')
		else:
			try:
				for f in self._filters:
					self._value = f.run(self._value)
			except ValidationError as e:
				self._valid = False
				self._errors.append(e.message)
			else:
				self._valid = True

		return self._valid

	def require(self, value=True):
		if self._required is None:
			self._required = value
		return self

	def blank(self, value=True):
		if self._blank is None:
			self._blank = value
		return self

	def alt(self, alt_name):
		self._schema.add_field(alt_name, self)
		return self

	def match(self, *other_fields):
		if not self._match:
			self._match = other_fields
		return self

	def __call__(self, *args, **kwargs):
		return self

	def __getattr__(self, name):
		fxn, pre, post = lookup(name)
		if not fxn:
			raise RuntimeError('Filter %s is undefined' % name)
		
		if pre:
			pref = Filter(self, pre)
			self._filters.append(pref)

		f = Filter(self, fxn)
		self._filters.append(f)

		if post:
			postf = Filter(self, post)
			self._filters.append(postf)

		return f

class Filter(object):

	def __init__(self, field, fxn):
		self._field = field
		self._validation_fxn = fxn

	def __call__(self, *args, **kwargs):
		partial_fxn = partial(self._validation_fxn, *args, **kwargs)
		partial_fxn.__name__ = self._validation_fxn.__name__
		self._validation_fxn = partial_fxn
		return self._field

	def __repr__(self):
		return '[Filter - %r]' % self._validation_fxn.__name__

	def run(self, value):
		processed = self._validation_fxn(_value=value)
		return processed