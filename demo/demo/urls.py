# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import HomeView, ServerErrorView, ObjectDoesNotExistView, PermissionDeniedView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

# urlpatterns = patterns('',
#     # Examples:
#     # url(r'^$', 'demo.views.home', name='home'),
#     # url(r'^demo/', include('demo.foo.urls')),
#
#     # Uncomment the admin/doc line below to enable admin documentation:
#     # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
#
#     # Uncomment the next line to enable the admin:
#     # url(r'^admin/', include(admin.site.urls)),
# )

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^permission_denied$', PermissionDeniedView.as_view(), name='permission_denied'),
    url(r'^object_does_not_exist$', ObjectDoesNotExistView.as_view(), name='object_does_not_exist'),
    url(r'^server_error$', ServerErrorView.as_view(), name='server_error'),
)
