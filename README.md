Class based permissions for Django models
=========================================

Simple class based permissions.

Installation
------------
1. Install using pip:

        pip install django-perm

2. In settings.py:

        # Add to INSTALLED_APPS

        'perm',

        # Add to MIDDLEWARE_CLASSES

        'perm.middleware.ModelPermissionsMiddleware',

        # Add to AUTHENTICATION_BACKENDS

        'perm.backends.ModelPermissionBackend',

Questions
---------

Do you have a question about the usage of this toolkit in your Django project? Please ask it on StackOverflow.com so others can help out and/or learn. Tag your question `django-perm` if possible.

    http://stackoverflow.com/

Bugs and requests
-----------------

If you have found a bug or a request for additional functionality, please use the issue tracker on GitHub.

    https://github.com/dyve/django-perm/issues

About
-----

django-bootstrap-toolkit is written by Dylan Verheul (dylan@dyve.net).

License
-------

You can use this under Apache 2.0. See LICENSE file for details.
