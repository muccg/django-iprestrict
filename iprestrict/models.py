from django.db import models
import re

from iprestrict import ip_utils as ipu

class IPGroup(models.Model):
    class Meta:
        verbose_name = "IP Group"

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def ranges(self, ip_type='ipv4'):
        if not hasattr(self, '_ranges'):
            self._ranges = { 'ipv4': [], 'ipv6': [] }
            for r in self.iprange_set.all():
                self._ranges[r.ip_type].append(r)
        return self._ranges[ip_type]

    def matches(self, ip):
        ip_type = ipu.get_version(ip)
        for r in self.ranges(ip_type):
            if ip in r:
                return True
        return False

    def __unicode__(self):
        return self.name

class IPRange(models.Model):
    class Meta:
        verbose_name = "IP Range"

    ip_group = models.ForeignKey(IPGroup)
    first_ip = models.GenericIPAddressField()
    last_ip = models.GenericIPAddressField(null=True, blank=True)

    @property
    def start(self):
        return ipu.to_number(self.first_ip)

    @property
    def end(self):
        if self.last_ip is None:
            return self.start
        return ipu.to_number(self.last_ip)

    @property
    def ip_type(self):
        if not self.first_ip: 
            return ''
        return ipu.get_version(self.first_ip)

    def __contains__(self, ip):
        ip_nr = ipu.to_number(ip)
        return self.start <= ip_nr <= self.end 

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
    rank = models.IntegerField()

    @property
    def regex(self):
        if not hasattr(self, '_regex'):
            self._regex = re.compile(self.url_pattern)
        return self._regex

    def matches_url(self, url):
        if self.url_pattern == 'ALL':
            return True
        else:
            return (self.regex.match(url) is not None)

    def matches_ip(self, ip):
        return self.ip_group.matches(ip)

    def is_restricted(self):
        return self.action != 'A'

    def is_allowed(self):
        return self.action == 'A'
    is_allowed.boolean = True
    is_allowed.short_description = 'Is allowed?'

    def swap_with_rule(self, other):
        other.rank, self.rank = self.rank, other.rank
        other.save()
        self.save()

    def move_up(self):
        rules_above = Rule.objects.filter(rank__lt = self.rank).order_by('-rank')
        if len(rules_above) == 0:
            return
        self.swap_with_rule(rules_above[0])

    def move_down(self):
        rules_below = Rule.objects.filter(rank__gt = self.rank)
        if len(rules_below) == 0:
            return
        self.swap_with_rule(rules_below[0])

    def save(self, *args, **kwargs):
        if self.rank is None:
            max_aggr = Rule.objects.filter(rank__lt = 65000).aggregate(models.Max('rank'))
            max_rank = max_aggr.get('rank__max')
            if max_rank is None:
                max_rank = 0
            self.rank = max_rank + 1
        super(Rule, self).save(*args, **kwargs)

