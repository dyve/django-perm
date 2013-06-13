from __future__ import unicode_literals

from django.db.models import Model, get_model as django_get_model
from django.utils.translation import ugettext as _

from perm.exceptions import PermAppException



def get_model(model, raise_exception = False):
    if isinstance(model, basestring):
        app_name, model_name = model.split('.')
        model = django_get_model(app_name, model_name)
    try:
        is_model = issubclass(model, Model)
    except TypeError:
        is_model = False
    if not is_model:
        model = None
        if raise_exception:
            raise PermAppException(_('%(model)s is not a Django Model class.' % {
                'model': model
            }))
    return model
