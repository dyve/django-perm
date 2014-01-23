from __future__ import unicode_literals

from django.db.models.query import EmptyQuerySet
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from perm.exceptions import PermAppException, PermQuerySetNotFound
from perm.utils import get_model


class ModelPermissionsManager(object):
    """
    Singleton object to hold ModelPermissions classes for objects
    """

    _registry = {}

    def register(self, model, permissions_class):
        model = get_model(model)
        self._registry[model] = permissions_class
        return model

    def register_permissions_class(self, permissions_class, model):
        self.register(model, permissions_class)
        return permissions_class

    def get_permissions(self, model, user_obj, perm, obj=None, raise_exception=False):
        model = get_model(model)
        permissions_checker_class = self._registry.get(model, None)
        if not permissions_checker_class:
            if raise_exception:
                raise PermAppException(_('No permissions registered for %(model)s.' % {'model': model}))
            return None
        permissions = permissions_checker_class(model, user_obj, perm, obj)
        return permissions


class ModelPermissions(object):
    """
    Class is instantiated once a permission has to be checked.
    The check itself is done by calling the has_perm() method.
    """
    model = None
    user = None
    perm = None
    obj = None

    def __init__(self, model, user_obj, perm, obj=None, *args, **kwargs):
        """
        Set the properties
        """
        super(ModelPermissions, self).__init__(*args, **kwargs)
        self.model = model
        self.user = user_obj
        self.obj = obj
        self.perm = perm

    def get_queryset(self):
        """
        Get method get_queryset_perm_PERM or return None
        """
        try:
            method = getattr(self, 'get_queryset_perm_%s' % self.perm)
        except AttributeError:
            raise PermQuerySetNotFound(_('Permissions for %(model)s do not include queryset for %(perm)s.' % {
                'model': self.model,
                'perm': self.perm
            }))
        return method()

    def _has_perm_using_method(self):
        """
        Test the method has_perm_PERM()
        """
        try:
            method = getattr(self, 'has_perm_%s' % self.perm)
        except AttributeError:
            return False
        return method()

    def _has_perm_using_queryset(self):
        """
        Test to see if obj appears in get_perm_PERM_queryset()
        """
        try:
            return self.get_queryset().filter(pk=self.obj.pk).exists()
        except PermQuerySetNotFound:
            return False

    def has_perm(self):
        """
        Test using direct method and queryset
        """
        return self._has_perm_using_method() or self._has_perm_using_queryset()


def load_permissions():
    """
    This is called once from the ModelPermissionsMiddleware.__init__ to discover all permissions in all applications
    """
    try:
        if load_permissions.done:
            return
    except AttributeError:
        pass
    load_permissions.done = True
    for app in settings.INSTALLED_APPS:
        try:
            __import__('%s.permissions' % app)
        except ImportError:
            pass


# Instantiate the singleton
permissions_manager = ModelPermissionsManager()
