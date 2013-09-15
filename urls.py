from django.conf.urls import patterns, include, url

from .views import *

urlpatterns = patterns('',

	url(r'^is_logged_in', is_logged_in),
	url(r'^logout', 'django.contrib.auth.views.logout', {'next_page': '/showform/events/'}),
    url(r'^login', jlogin),
    url(r'^testcookie', testcookie),
)