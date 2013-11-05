# Changelog
current version: 0.1.1

### v0.1.1
* Changed the result printer so that it uses the "canonical name" always.

## v0.1.0
* Major internal refactor of the Schema class, API of course remains unbroken.
* Addition of several options: ``` Schema.strip_missing ```, ``` Schema.strip_blank ```, ``` Schema.alts ```
* Better pathway for handling missing, blank and required value distinction.
* Performance enhancements
* Updated README

### v0.0.12
* Required behavior bugfix

### v0.0.11
* Fixed a behavior with required field checking so that missing fields are not validated. Eventually might refactor the entire way the schema processes input...

### v0.0.10
* Renamed ``` Schema.name ``` to ``` Schema.schema_name ``` to eliminate the collision caused due to the frequent and obvious need for a field called "name".

### v0.0.9
* ``` strings._pre_hook ``` now converts ``` NoneType ``` to empty string if received.

### v0.0.8
* Added the ``` strings.key_lookup ``` filter. This is used for creating lookup dictionaries to convert input values to logical equivalents. For example, ``` schema.state_name.key_lookup({'MA': 'Massachusetts'}) ``` would convert an incoming value of "MA" to "Massachusetts". You can set missing key behavior via ``` nomatch ``` param.

### v0.0.7
* Added support for dict-based schema definitions via ``` Schema.from_dict(dict_scheme, **kwargs) ```
* Fixed ``` collections.drop_keys ``` and ``` collections.contains ``` to support ``` *args ``` for convenience.

### v0.0.6
* BUGFIX: validating required fields now properly recognizes fields supplied with alternate names

### v0.0.5
* Added the ``` casting.decimal ``` filter and tests.
* Added ``` Schema.results ``` not sure why this was not added earlier. Brain fail.
* Added full unicode support via ``` Schema(force_unicode=True) ```. Leaving this set to True will
cause the schema and the data input to be intelligently casted to unicode where appropriate.

### v0.0.4
* Added the ```money.credit_card``` filter and tests
* Added a test for ```logical.constant```
* Added the ```casting.none``` filter
* Added the ```match```, ```require```, ```blank```, and ```extra``` options to the schema.
* Added a LICENSE...
* If a ```Field``` is present, blank is NOT allowed by default. However, ```Field``` is OPTIONAL by default.
* Removed the ```casting.jsbool``` filter because of redundant functionality. Just use ```casting.none``` in conjunction with ```casting.strbool```. You will need to make sure to ```Field.blank(True)``` if you want to accept NoneType values such as 'undefined'.

### v0.0.3
* Added a prehook ```_strip``` option for ALL string validators. The option is ```True``` by default and will invoke the ```strip()``` validator on all string validators.
* Added the following filter modules ```[casting, chrono, collection, logical]```
* Added tests for ```strings.canonize``` and ```strings.slugify```
* Fixed the ```web.ipv4``` validator so that it actually verifies the values of the octets :0
* Added the following filters: ```[casting.boolean, casting.jsbool, casting.strbool, casting.integer, casting.longint, casting.numeric]```
* filters continued: ```[web.url, casting.string, chrono.date, chrono.time, chrono.datetime, chrono.time_before, chrono.time_after, chrono.time_between]```
* Added a schema-level ```match``` option used like so: ```s = Schema('my_schema', match={'password': 'password_confirm'})```
* Changed the name of the ```strings.numeric``` validator to ```strings.numeric_string``` to differentiate it from the ```casting.numeric``` filter. Remember that filters are thrust into a global namespace as part of the API's brevity.
* Added tests for the chrono module
* Added in travis-ci with coveralls and pypins