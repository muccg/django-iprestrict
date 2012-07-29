from django.conf.urls import patterns, include, url

urlpatterns = patterns('iprestrict.views',
    url(r'^move_rule_up/(?P<rule_id>\d+)[/]?$', 'move_rule_up'),
    url(r'^move_rule_down/(?P<rule_id>\d+)[/]?$', 'move_rule_down'),
    url(r'^reload_rules[/]?$', 'reload_rules'),
)

