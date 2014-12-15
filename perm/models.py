# -*- coding: utf-8 -*-
import django
from django.utils.module_loading import module_has_submodule


def autodiscover():
    """
    This is called once to discover all permissions in all applications
    """
    try:
        if autodiscover.done:
            return
    except AttributeError:
        pass
    autodiscover.done = True

    if django.VERSION < (1, 7):
        from django.utils.importlib import import_module
        mods = [(app, import_module(app)) for app in django.conf.settings.INSTALLED_APPS]
    else:
        from importlib import import_module
        from django.apps import apps
        mods = [(app_config.name, app_config.module) for app_config in apps.get_app_configs()]

    for (app, mod) in mods:
        # Attempt to import the app's permissions module.
        module = '%s.permissions' % app
        try:
            import_module(module)
        except ImportError:
            # Decide whether to bubble up this error. If the app just
            # doesn't have an translation module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'permissions'):
                raise


if django.VERSION < (1, 7):
    autodiscover()