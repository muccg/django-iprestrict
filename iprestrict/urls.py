from django.conf.urls import url
from .views import test_rules_page, test_match, reload_rules
from .views import move_rule_up, move_rule_down

app_name = "iprestrict"
urlpatterns = [
    url(r'^$', test_rules_page),
    url(r'^move_rule_up/(?P<rule_id>\d+)[/]?$', move_rule_up),
    url(r'^move_rule_down/(?P<rule_id>\d+)[/]?$', move_rule_down),
    url(r'^reload_rules[/]?$', reload_rules),
    url(r'^test_match[/]?$', test_match),
]
