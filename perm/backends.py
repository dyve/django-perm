from django.utils.translation import ugettext_lazy
from django.db.models import Model

from .exceptions import PermAppException
from .permissions import permissions_manager


class ModelPermissionBackend(object):

    supports_object_permissions = True
    supports_anonymous_user = True
    supports_inactive_user = True

    def authenticate(self, username, password):
        """
        This backend does not authenticate
        """
        return None

    def has_perm(self, user_obj, perm, obj):

        # Non-existing and inactive users never get permission
        if not user_obj or not user_obj.is_active:
            return False

        # If obj is an instance, get the model class
        if isinstance(obj, Model):
            model = obj.__class__
        else:
            model = obj
            obj = None

        # If permission is in dot notation, make sure permission and object application are the same
        # and keep only the last part of the permission (without application name)
        perm_parts = perm.split('.')
        if len(perm_parts) > 1:
            perm_app, perm = perm_parts
            model_app = model._meta.app_label
            if perm_app != model_app:
                raise PermAppException(
                    ugettext_lazy("App mismatch, perm has '%(perm_app)s' and model has '%(model_app)s'" % {
                        'perm_app': perm_app,
                        'model_app': model_app,
                    })
                )

        # Get the ModelPermissions object
        object_permissions = permissions_manager.get_permissions(model, user_obj, perm, obj)

        # No ModelPermissions means no permission
        if not object_permissions:
            return False

        # Check the permissions
        return object_permissions.has_perm()
