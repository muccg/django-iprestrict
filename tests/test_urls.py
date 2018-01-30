# -*- coding: utf-8 -*-
# This file is to be used for testing only
from __future__ import unicode_literals

import django
from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
import iprestrict.urls

admin.autodiscover()

app_name = "iprestrict"
# Following this branch on v1.0 will not throw, it simply won't interoperate with the url resolver when used.
# Need to detect up front.
if django.VERSION[0] == 2:
	urlpatterns = [
	    url(r'^iprestrict/', include('iprestrict.urls', namespace='iprestrict')),
	    url(r'^admin/', admin.site.urls),
	] + staticfiles_urlpatterns()
else:
	urlpatterns = [
	    url(r'^iprestrict/', include(iprestrict.urls.urlpatterns, namespace='iprestrict')),
		url(r'^admin/', include(admin.site.urls)),
	] + staticfiles_urlpatterns()
