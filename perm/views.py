from django.views.generic import DetailView, UpdateView, CreateView

from .http import HttpForbidden


class PermSingleObjectMixin(object):

    perm = None

    def get_object(self, *args, **kwargs):
        if isinstance(self, CreateView):
            obj = self.model
        else:
            obj = super(PermSingleObjectMixin, self).get_object(*args, **kwargs)
        if self.perm and not self.request.user.has_perm(self.perm, obj):
            raise HttpForbidden()
        return obj


class PermDetailView(PermSingleObjectMixin, DetailView):

    perm = 'view'


class PermUpdateView(PermSingleObjectMixin, UpdateView):

    perm = 'change'


class PermCreateView(PermSingleObjectMixin, CreateView):

    perm = 'create'