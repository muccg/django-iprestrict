# -*- coding: utf-8 -*-
# This file is to be used for testing only
from __future__ import unicode_literals

import django

from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

try:
    from django.urls import include, path
    PRE_DJANGO_2 = False
except ImportError:
    from django.conf.urls import include, url
    PRE_DJANGO_2 = True

import iprestrict.urls


if PRE_DJANGO_2:
	urlpatterns = [
        url(r'^iprestrict/', include('iprestrict.urls')),
        url(r'^admin/', include(admin.site.urls)),
	]
else:
	urlpatterns = [
	    path('iprestrict/', include('iprestrict.urls')),
	    path('admin/', admin.site.urls),
	]

urlpatterns += staticfiles_urlpatterns()
