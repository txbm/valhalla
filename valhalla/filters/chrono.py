from .. import ValidationError

# attempts to return a validate Date/DateTime object
def date(): pass

# attempts to return a validate Time/Timestamp type object
def time(): pass

# validates that datetime is before specified datetime
def before(): pass

# validates that datetime is after specified datetime
def after(): pass

# validates that datetime is between specified times
def between(): pass

# validates that delta between two times is within allowed range
def delta_range(): pass