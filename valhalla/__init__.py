from functools import partial

from . import filters

class ValidationError(Exception): pass

class Schema(object):

	def __init__(self):
		self._fields = []

	def __getattr__(self, attr):
		return self.add_field(attr, Field(self))

	def add_field(self, name, field):
		self._fields[name] = field
		setattr(self, name, field)
		return field

	def validate(self, data_dict, **kwargs):
		for field_name, input_value in data_dict.iteritems():
			try:
				field = self._fields[field_name]
			except KeyError:
				continue
			
			field.reset(input_value)
			field.validate()

class Field(object):

	def __init__(self, schema):
		self._schema = schema
		self._original_value = None
		self._value = None
		self._filters = []
		self._valid = False
		self._errors = []

		self._required = False
		self._alternate_name = None

	def reset(self, value=None):
		self._valid = False
		self._errors = []
		self._original_value = self._value = value

	def validate(self):
		try:
			for f in self._filters:
				self._value = f.run(self._value)
		except ValidationError as e:
			self._valid = False
			self._errors.append(e.message)

	def __call__(self, *args, **kwargs):
		option_alias_map = {
			'req': '_required',
			'alt': '_alternate_name',
		}
	
		for k, v in kwargs.iteritems():
			if k in option_alias_map:
				setattr(self, option_alias_map[k], v)

		if self._alternate_name:
			self._schema.add_field(self._alternate_name, self)

	def __getattr__(self, name):
		def _search_module(m):
			return getattr(m, filter_name, False)
		try:
			fxn = filter([_search_module(m) for m in filters])[0]
			f = Filter(self, fxn)
			self._filters.append(f)
			return f
		finally:
			raise RuntimeError('Filter %s is undefined' % filter_name)

class Filter(object):

	def __init__(self, field, fxn):
		self._field = field
		self._validation_fxn = fxn

	def run(self, value):
		return self._validation_fxn(_value=value)

	def __call__(self, *args, **kwargs):
		self._validation_fxn = partial(self._validation_fxn, *args, **kwargs)
		return self._field