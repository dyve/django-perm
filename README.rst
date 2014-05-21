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

        # Add to AUTHENTICATION_BACKENDS

        'perm.backends.ModelPermissionBackend',


Usage
-----

In your Django app, create a file ``permissions.py``. Its content might look like this:

    from perm.decorators import permissions_for
    from perm.permissions import ModelPermissions

    from .models import Foo


    @permissions_for(Foo)
    class ProjectPermissions(FooPermissions):

        def has_perm_wiggle(self):
            # Let's ask the Foo object
            return self.obj.user_can_wiggle(self.user)

        def get_perm_change_queryset(self):
            # Foo objects can be changed by their owners
            return Foo.objects.filter(user=self.user)


Questions
---------

Do you have a question about ``django-perm``? Please ask it on StackOverflow.com so others can help out and/or learn. Tag your question ``django-perm`` if possible.

http://stackoverflow.com/


Bugs and requests
-----------------

If you have found a bug or a request for additional functionality, please use the issue tracker on GitHub.

https://github.com/dyve/django-perm/issues


About
-----

``django-perm`` is written by Dylan Verheul (dylan@dyve.net).


License
-------

You can use this under Apache 2.0. See LICENSE file for details.
