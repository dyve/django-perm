from __future__ import unicode_literals

from .permissions import permissions_manager


def get_perm_queryset(model, user, perm):
    permissions = permissions_manager.get_permissions(model, user, perm, raise_exception=True)
    return permissions.get_queryset(raise_exception=True)
