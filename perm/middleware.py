from django.core.exceptions import PermissionDenied

from .permissions import load_permissions
from .http import HttpException, HttpForbidden


class ModelPermissionsMiddleware(object):

    def __init__(self, *args, **kwargs):
        super(ModelPermissionsMiddleware, self).__init__(*args, **kwargs)
        # Run load_permissions exactly once
        load_permissions()

    def process_exception(self, request, exception):
        # Convert standard PermissionDenied to our own HttpForbidden
        if isinstance(exception, PermissionDenied):
            exception = HttpForbidden(unicode(exception))
        # Make our own HttpException return its response
        if isinstance(exception, HttpException):
            response = exception.render_to_reponse(request)
            if response:
                return response
        # Nothing more to do here
        return None