from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^polls/', include('polls.urls')),
    url(r'^iprestrict/', include('iprestrict.urls', namespace='iprestrict')),
    url(r'^admin/', include(admin.site.urls)),
]
