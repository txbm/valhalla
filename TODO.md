* Make a SQLAlchemy schema-builder that intelligently reads a SQLAlchemy model and builds a recommended schema.
* Add locale specification support to [date, time, datetime] validators so that ```field_name.date(locale='en_US')``` uses Python's built in locale support to provide the correct validation behavior
* Add support for default field values
* Refactor text(min_len, max_len) into str_len(min, max) as separate filter