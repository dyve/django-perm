from __future__ import unicode_literals

from django.db.models import Model
from django.db.models.loading import get_model
from django.utils.translation import ugettext as _

from .exceptions import PermAppException


def get_model_for_perm(model, raise_exception=False):
    if isinstance(model, basestring):
        # If model is a string, find the appropriate model class
        try:
            app_name, model_name = model.split('.')
        except ValueError:
            model_class = None
        else:
            try:
                model_class = get_model(app_name, model_name)
            except LookupError:
                model_class = None
    else:
        # Assume we have been given a model class or instance
        model_class = model

    # Test is this is an instance or subclass of Model
    try:
        is_model = issubclass(model_class, Model)
    except TypeError:
        is_model = False

    # Handle failure
    if not is_model:
        if raise_exception:
            raise PermAppException(_('%(model)s is not a Django Model class.' % {
                'model': model
            }))
        return None

    # Return the result
    return model_class
