# This file is to be used for testing only

from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
import iprestrict.urls

admin.autodiscover()

urlpatterns = [
    url(r'^iprestrict/', include(iprestrict.urls.urlpatterns)),
    url(r'^admin/', include(admin.site.urls)),
] + staticfiles_urlpatterns()
