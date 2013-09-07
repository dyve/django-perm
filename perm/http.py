from django.core.handlers.wsgi import STATUS_CODE_TEXT
from django.shortcuts import render

from .exceptions import PermException


class HttpException(PermException):
    message = ''
    status_code = 500 # because this means you've instantiated the wrong thing
    headers = {} # extra headers for the final HTTP response

    def __init__(self, *args, **kwargs):
        super(HttpException, self).__init__(*args, **kwargs)
        self.message = unicode(self)

    def get_templates(self):
        # Get template
        return ["perm/http_%s.html" % self.status_code, "perm/http.html"]

    def get_context(self):
        return {
            'message': self.message,
            'http_status_code': self.status_code,
            'http_status_text': STATUS_CODE_TEXT.get(self.status_code, 'UNKNOWN'),
            'http_exception': self,
        }

    def render_to_reponse(self, request):
        # Basic response
        response = render(request, self.get_templates(), self.get_context())
        # Set status code
        response.status_code = self.status_code
        # Add headers
        if self.headers:
            for k, v in self.headers.items():
                response[k] = v
        # Augment response
        self.augment_response(response)
        # Return result
        return response

    def augment_response(self, response):
        # Overwrite this to augment the response
        pass


class HttpBadRequest(HttpException):
    status_code = 400


class HttpForbidden(HttpException):
    status_code = 403
