import re
from django.core.urlresolvers import reverse
from django.db import models
from datetime import datetime
from . import ip_utils as ipu


class IPGroup(models.Model):
    class Meta:
        verbose_name = "IP Group"

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __init__(self, *args, **kwargs):
        models.Model.__init__(self, *args, **kwargs)
        self.load_ranges()

    def load_ranges(self):
        self._ranges = {'ipv4': [], 'ipv6': []}
        for r in self.iprange_set.all():
            self._ranges[r.ip_type].append(r)

    def ranges(self, ip_type='ipv4'):
        return self._ranges[ip_type]

    def matches(self, ip):
        ip_type = ipu.get_version(ip)
        for r in self.ranges(ip_type):
            if ip in r:
                return True
        return False

    def ranges_str(self):
        return ', '.join([str(r) for r in self.ranges()])

    def __str__(self):
        return self.name

    __unicode__ = __str__


class IPRange(models.Model):
    class Meta:
        verbose_name = "IP Range"

    ip_group = models.ForeignKey(IPGroup)
    first_ip = models.GenericIPAddressField()
    cidr_prefix_length = models.PositiveSmallIntegerField(null=True, blank=True)
    last_ip = models.GenericIPAddressField(null=True, blank=True)

    @property
    def start(self):
        if self.cidr_prefix_length is not None:
            start, end = ipu.cidr_to_range(self.first_ip,
                                           self.cidr_prefix_length)
            return start
        else:
            return ipu.to_number(self.first_ip)

    @property
    def end(self):
        if self.last_ip is not None:
            return ipu.to_number(self.last_ip)
        if self.cidr_prefix_length is not None:
            start, end = ipu.cidr_to_range(self.first_ip,
                                           self.cidr_prefix_length)
            return end
        return self.start

    @property
    def ip_type(self):
        if not self.first_ip:
            return ''
        return ipu.get_version(self.first_ip)

    def __contains__(self, ip):
        ip_nr = ipu.to_number(ip)
        return self.start <= ip_nr <= self.end

    def __str__(self):
        result = str(self.first_ip)
        if self.cidr_prefix_length is not None:
            result += '/' + str(self.cidr_prefix_length)
        elif self.last_ip is not None:
            result += '-' + str(self.last_ip)
        return result

    __unicode__ = __str__


class Rule(models.Model):
    class Meta:
        ordering = ['rank', 'id']

    ACTION_CHOICES = (
        ('A', 'ALLOW'),
        ('D', 'DENY')
    )

    url_pattern = models.CharField(max_length=500)
    ip_group = models.ForeignKey(IPGroup, default=1)
    action = models.CharField(max_length=1, choices=ACTION_CHOICES, default='D')
    rank = models.IntegerField(blank=True)

    @property
    def regex(self):
        if not hasattr(self, '_regex'):
            self._regex = re.compile(self.url_pattern)
        return self._regex

    def matches_url(self, url):
        if self.url_pattern == 'ALL':
            return True
        else:
            return self.regex.match(url) is not None

    def matches_ip(self, ip):
        return self.ip_group.matches(ip)

    def is_restricted(self):
        return self.action != 'A'

    def is_allowed(self):
        return self.action == 'A'
    is_allowed.boolean = True
    is_allowed.short_description = 'Is allowed?'

    def action_str(self):
        return 'Allowed' if self.is_allowed() else 'Denied'

    def swap_with_rule(self, other):
        other.rank, self.rank = self.rank, other.rank
        other.save()
        self.save()

    def move_up(self):
        rules_above = Rule.objects.filter(rank__lt=self.rank).order_by('-rank')
        if len(rules_above) == 0:
            return
        self.swap_with_rule(rules_above[0])

    def move_up_url(self):
        url = reverse('iprestrict.views.move_rule_up', args=[self.pk])
        return '<a href="%s">Move Up</a>' % url
    move_up_url.allow_tags = True
    move_up_url.short_description = 'Move Up'

    def move_down_url(self):
        url = reverse('iprestrict.views.move_rule_down', args=[self.pk])
        return '<a href="%s">Move Down</a>' % url
    move_down_url.allow_tags = True
    move_down_url.short_description = 'Move Down'

    def move_down(self):
        rules_below = Rule.objects.filter(rank__gt=self.rank)
        if len(rules_below) == 0:
            return
        self.swap_with_rule(rules_below[0])

    def save(self, *args, **kwargs):
        if self.rank is None:
            max_aggr = Rule.objects.filter(rank__lt=65000).aggregate(models.Max('rank'))
            max_rank = max_aggr.get('rank__max')
            if max_rank is None:
                max_rank = 0
            self.rank = max_rank + 1
        super(Rule, self).save(*args, **kwargs)


class ReloadRulesRequest(models.Model):
    at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def request_reload(cls):
        rrs = ReloadRulesRequest.objects.all()
        if len(rrs) > 0:
            obj = rrs[0]
            obj.at = datetime.now()
            obj.save()
        else:
            cls.objects.create()

    @staticmethod
    def last_request():
        result = None
        rrs = ReloadRulesRequest.objects.all()
        if len(rrs) > 0:
            result = rrs[0].at
        return result
