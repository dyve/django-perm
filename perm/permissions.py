from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from perm.exceptions import PermAppException, PermQuerySetNotFound
from perm.utils import get_model_for_perm


class ModelPermissionsManager(object):
    """
    Singleton object to hold ModelPermissions classes for objects
    """
    _registry = {}

    def register(self, model, permissions_class):
        model = get_model_for_perm(model)
        self._registry[model] = permissions_class
        return model

    def register_permissions_class(self, permissions_class, model):
        self.register(model, permissions_class)
        return permissions_class

    def get_permissions(self, model, user_obj, perm, obj=None, raise_exception=False):
        model = get_model_for_perm(model)
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
        super(ModelPermissions, self).__init__()
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
        except (AttributeError, PermQuerySetNotFound):
            return False

    def has_perm(self):
        """
        Test using direct method and queryset
        """
        return self._has_perm_using_method() or self._has_perm_using_queryset()


# Instantiate the singleton
permissions_manager = ModelPermissionsManager()
