.. :changelog:

History
-------


2.4.1 (2014-12-15)
++++++++++++++++++

* Fixed bug in autodiscover


2.4.0 (2014-12-15)
++++++++++++++++++

* Isolated has_perm in PermSingleObjectMixin


2.3.0 (2014-12-08)
++++++++++++++++++

* Made tests work in Django 1.7
* Modified Travis matrix


2.2.1 (2014-08-28)
++++++++++++++++++

* Fixed bug in `{% ifperm ... %}` tag and added tests


2.2.0 (2014-08-28)
++++++++++++++++++

* New `{% perm ... %}` template tag with optional `as varname` to write to context


2.1.0 (2014-05-21)
++++++++++++++++++

* Must load via urls now, documented this in README


2.0.2 (2014-05-21)
++++++++++++++++++

* Fix Travis CI


2.0.1 (2014-05-21)
++++++++++++++++++

* Now works with standard Django exception PermissionDenied


2.0.0 (2014-05-21)
++++++++++++++++++

* Now works without its own middleware
