# Changelog
current version: 0.0.3

## v0.0.3

* Added a prehook ```_strip``` option for ALL string validators. The option is ```True``` by default and will invoke the ```strip()``` validator on all string validators.
* Added the following filter modules ```[casting, chrono, collection, logical]```
* Added tests for ```strings.canonize``` and ```strings.slugify```
* Fixed the ```web.ipv4``` validator so that it actually verifies the values of the octets :0
* Added the following filters: ```[casting.boolean, casting.jsbool, casting.strbool, casting.integer, casting.longint, casting.numeric]```
* filters continued: ```[web.url]```
* Added a schema-level ```match``` option used like so: ```s = Schema('my_schema', match={'password': 'password_confirm'})```