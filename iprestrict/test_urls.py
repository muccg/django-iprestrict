# This file is to be used for testing only

from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('iprestrict.views',
    url(r'^iprestrict/$', 'test_rules_page'),
    url(r'^iprestrict/move_rule_up/(?P<rule_id>\d+)[/]?$', 'move_rule_up'),
    url(r'^iprestrict/move_rule_down/(?P<rule_id>\d+)[/]?$', 'move_rule_down'),
    url(r'^iprestrict/reload_rules[/]?$', 'reload_rules'),
    url(r'^iprestrict/test_match[/]?$', 'test_match'),
)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

