from functools import partial

def schema():
	return type('schema', (), {
		'__getattribute__': _add_field,
		'validate': _validate_schema
	})

def _field():
	return type('field', (), {
		'_schema': None,
		'_original_value': None,
		'_value': None,
		'_required': False,
		'_alternate_name': None,
		'_filters': [],
		'__call__': _setup_field
		'__getattribute__': _add_filter
	})

def _filter():
	return type('filter', (), {
		'_field': None,
		'_validation_fxn': None,
		'__call__': _setup_filter
	})


def _validate_schema(schema, data_dict, **kwargs):
	for field_name, input_value in data_dict.iteritems():
		field = getattr(schema, field_name)
		if not field:
			continue # upgrade this later perhaps to store skipped values
		field._original_value = f._value = input_value

		for f in field._filters:
			field._value = f._validation_fxn(_value=field._value)



def _add_field(schema, field_name):
	f = _field()
	f._schema = schema
	setattr(schema, field_name, f)
	#return f

def _setup_field(field, *args, **kwargs):
	option_map = {
		'_required': 'req',
		'_alternate_name': 'alt',
	}
	
	for attr, opt in option_map.iteritems():
		setattr(field, attr, kwargs.get(opt))

	if field._alternate_name:
		setattr(field._schema, field._alternate_name, field)

def _add_filter(field, filter_name):
	from . import filters
	def _search_module(m):
		return getattr(m, filter_name, False)
	try:
		fxn = filter([_search_module(m) for m in filters])[0]
		f = _filter()
		f._validation_fxn = fxn
		f._field = field
		field._filters.append(f)
		return f
	finally:
		raise RuntimeError('Filter %s is undefined' % filter_name)

def _setup_filter(f1lter, *args, **kwargs):
	f1lter._validation_fxn = partial(f1lter._validation_fxn, *args, **kwargs)
	return f1lter._field

# s = schema()
# s.first_name.text(min_length=3)