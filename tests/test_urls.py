# -*- coding: utf-8 -*-
# This file is to be used for testing only
from __future__ import unicode_literals


from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
import iprestrict.urls

admin.autodiscover()

app_name = "iprestrict"
urlpatterns = [
    url(r'^iprestrict/', include('iprestrict.urls', namespace='iprestrict')),
    url(r'^admin/', admin.site.urls),
] + staticfiles_urlpatterns()
