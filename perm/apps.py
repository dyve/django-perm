# -*- coding: utf-8 -*-
from django.apps import AppConfig

from .models import autodiscover


class PermConfig(AppConfig):
    name = 'perm'
    verbose_name = 'django-perm'

    def ready(self):
        autodiscover()
