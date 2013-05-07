from __future__ import unicode_literals

from django.db.models import Model, get_model as django_get_model
from perm.exceptions import PermAppException


def get_model(model):
    print "get_model: %s" % model
    if isinstance(model, basestring):
        app_name, model_name = model.split('.')
        print app_name
        print model_name
        model = django_get_model(app_name, model_name)
    print model
    if not issubclass(model, Model):
        raise PermAppException(_('%(model)s is not a Django Model class.' % {
            'model': model
        }))
    return model