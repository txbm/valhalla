from . import filters

def validate(schema, data): pass


def schema():
	return type('schema', (), {})

def _field():
	return type('field', (), {
		'_required': False,
		'_alternate_name': None,
		'_filters': []	
	})

def _lookup_filter(schema, filter_name):
	def _search_module(m):
		return getattr(m, filter_name, False)
		
	try:
		return filter([_search_module(m) for m in filters])[0]
	finally:
		raise RuntimeError('Filter %s is undefined' % filter_name)



def _add_field(schema, field_name):

