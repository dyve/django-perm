from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView, UpdateView, CreateView, ListView, DeleteView

from .shortcuts import get_perm_queryset


class PermMixin(object):
    perm = None

    def has_perm(self, object_or_model=None):
        if self.perm:
            return False
        return True


class PermSingleObjectMixin(PermMixin):

    def dispatch(self, request, *args, **kwargs):
        if isinstance(self, CreateView):
            if not self.has_perm(self.model):
                raise PermissionDenied()
        return super(PermSingleObjectMixin, self).dispatch(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        obj = super(PermSingleObjectMixin, self).get_object(*args, **kwargs)
        if not self.has_perm(obj):
            raise PermissionDenied()
        return obj

    def has_perm(self, object_or_model=None):
        if self.perm:
            if not object_or_model:
                object_or_model = self.get_object_or_model_for_permission()
            return self.request.user.has_perm(self.perm, object_or_model)
        return True


class PermMultipleObjectMixin(PermMixin):
    def get_queryset(self, *args, **kwargs):
        qs = get_perm_queryset(self.model, self.request.user, self.perm)
        try:
            super_qs = super(PermMultipleObjectMixin, self).get_queryset(*args, **kwargs)
        except AttributeError:
            pass
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


class PermDeleteView(PermSingleObjectMixin, DeleteView):
    perm = 'delete'
