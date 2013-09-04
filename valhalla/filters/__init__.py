from importlib import import_module

__all__ = [
	'strings'
]

def lookup(name):
	mod, fxn = None, None
	try:
		for m in __all__:
			mod_name = 'valhalla.filters.%s' % m
			mod = import_module(mod_name)
	except ImportError: pass
	
	try:
		fxn = getattr(mod, name)
	finally:
		return fxn
