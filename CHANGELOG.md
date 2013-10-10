# Changelog
current version: 0.0.3

## v.0.0.4
* Added the ```money.credit_card``` validator and tests

## v0.0.3

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