from .. import ValidationError

_cc_num_regexes = [
	
]

# accepts a tuple (number, exp_date, csc)
def credit_card(brands=[], _value=(), *args, **kwargs):
	if type(_value) is not tuple:
		raise ValidationError('This validator requires a (number, exp_date, csc) tuple.')