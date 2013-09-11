from django.views.generic import DetailView, UpdateView, CreateView, ListView, DeleteView

from .http import HttpForbidden
from .shortcuts import get_perm_queryset


class PermMixin(object):
    perm = None


class PermSingleObjectMixin(PermMixin):
    def dispatch(self, request, *args, **kwargs):
        if isinstance(self, CreateView):
            obj = self.model
            print obj
            if self.perm and not self.request.user.has_perm(self.perm, obj):
                raise HttpForbidden()
        return super(PermSingleObjectMixin, self).dispatch(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        if isinstance(self, CreateView):
            obj = self.model
        else:
            obj = super(PermSingleObjectMixin, self).get_object(*args, **kwargs)
        if self.perm and not self.request.user.has_perm(self.perm, obj):
            raise HttpForbidden()
        return obj


class PermMultipleObjectMixin(PermMixin):
    def get_queryset(self, *args, **kwargs):
        qs = get_perm_queryset(self.model, self.request.user, self.perm)
        try:
            super_qs = super(PermMultipleObjectMixin, self).get_queryset(*args, **kwargs)
        except AttributeError:
            super_qs = None
        else:
            qs = qs.filter(pk__in=super_qs)
        return qs


class PermDetailView(PermSingleObjectMixin, DetailView):
    perm = 'view'


class PermUpdateView(PermSingleObjectMixin, UpdateView):
    perm = 'change'


class PermCreateView(PermSingleObjectMixin, CreateView):
    perm = 'create'


class PermListView(PermMultipleObjectMixin, ListView):
    perm = 'list'


class PermListView(PermSingleObjectMixin, DeleteView):
    perm = 'delete'