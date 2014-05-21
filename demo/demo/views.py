# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = 'demo/home.html'


class ExceptionView(HomeView):
    exception_class = None

    def get_context_data(self, **kwargs):
        context = super(ExceptionView, self).get_context_data(**kwargs)
        if self.exception_class:
            raise self.exception_class('Raised by an ExceptionView')
        return context


class ObjectDoesNotExistView(ExceptionView):
    exception_class = ObjectDoesNotExist


class PermissionDeniedView(ExceptionView):
    exception_class = PermissionDenied


class ServerErrorView(ExceptionView):

    def get_context_data(self, **kwargs):
        context = super(ServerErrorView, self).get_context_data(**kwargs)
        context['fail'] = None + True + 'fail' + {}
        return context

