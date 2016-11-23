# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from . import ip_utils as ipu
from .geoip import get_geoip, NO_COUNTRY


TYPE_LOCATION = 'location'
TYPE_RANGE = 'range'


geoip = get_geoip()


class IPGroupManager(models.Manager):
    def get_queryset(self):
        qs = super(IPGroupManager, self).get_queryset()
        if self.model.TYPE is not None:
            return qs.filter(type=self.model.TYPE)
        return qs


class IPGroup(models.Model):
    TYPE_CHOICES = ((TYPE_LOCATION, 'Location based'),
                    (TYPE_RANGE, 'Range based'))
    TYPE = None

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=10, default=TYPE_RANGE, choices=TYPE_CHOICES)

    class Meta:
        verbose_name = 'IP Group'

    objects = IPGroupManager()

    def __init__(self, *args, **kwargs):
        super(IPGroup, self).__init__(*args, **kwargs)
        self.load()

    def load(self):
        pass

    def save(self, *args, **kwargs):
        self.type = self.TYPE
        super(IPGroup, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    __unicode__ = __str__


def typed_ip_group(ip_group):
    obj = None
    if ip_group.type == TYPE_RANGE:
        obj = RangeBasedIPGroup(pk=ip_group.pk)
    elif ip_group.type == TYPE_LOCATION:
        obj = LocationBasedIPGroup(pk=ip_group.pk)
    else:
        raise ValueError("Invalid type '%s'" % ip_group.type)
    obj.__dict__.update(ip_group.__dict__)
    return obj


class RangeBasedIPGroup(IPGroup):
    TYPE = TYPE_RANGE

    class Meta:
        proxy = True
        verbose_name = 'IP Group'

    def load_ranges(self):
        self._ranges = {'ipv4': [], 'ipv6': []}
        for r in self.iprange_set.all():
            self._ranges[r.ip_type].append(r)

    load = load_ranges

    def ranges(self, ip_type='ipv4'):
        return self._ranges[ip_type]

    def matches(self, ip):
        ip_type = ipu.get_version(ip)
        for r in self.ranges(ip_type):
            if ip in r:
                return True
        return False

    def details_str(self):
        return ', '.join([str(r) for r in self.ranges()])


class LocationBasedIPGroup(IPGroup):
    TYPE = TYPE_LOCATION

    class Meta:
        proxy = True
        verbose_name = 'Location Based IP Group'

    def load_locations(self):
        countries = ", ".join(self.iplocation_set.values_list('country_codes', flat=True)).split(', ')
        countries.sort()
        self._countries = ', '.join(countries)

    load = load_locations

    def matches(self, ip):
        country_code = geoip.country_code(ip) or NO_COUNTRY
        return country_code in self._countries

    def details_str(self):
        return self._countries


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


class IPLocation(models.Model):
    class Meta:
        verbose_name = "IP Location"

    ip_group = models.ForeignKey(IPGroup)
    country_codes = models.CharField(max_length=2000, help_text='Comma-separated list of 2 character country codes')

    def __contains__(self, country_code):
        return country_code in re.split(r'[^A-Z]+', self.country_codes)

    def __str__(self):
        return self.country_codes

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
    reverse_ip_group = models.BooleanField(default=False)
    action = models.CharField(max_length=1, choices=ACTION_CHOICES, default='D')
    rank = models.IntegerField(blank=True)

    def __init__(self, *args, **kwargs):
        super(Rule, self).__init__(*args, **kwargs)
        self.ip_group = typed_ip_group(self.ip_group)

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
        match = typed_ip_group(self.ip_group).matches(ip)
        if self.reverse_ip_group:
            return not match
        return match

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
        url = reverse('iprestrict:move_rule_up', args=[self.pk])
        return '<a href="%s">Move Up</a>' % url
    move_up_url.allow_tags = True
    move_up_url.short_description = 'Move Up'

    def move_down_url(self):
        url = reverse('iprestrict:move_rule_down', args=[self.pk])
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
            obj.at = timezone.now()
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
