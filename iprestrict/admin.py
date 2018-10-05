# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django import forms
import re
from . import ip_utils as ipu
from . import models
from .geoip import is_valid_country_code


NOT_LETTER = re.compile(r'[^A-Z]+')


@admin.register(models.Rule)
class RuleAdmin(admin.ModelAdmin):
    exclude = ('rank',)
    list_display = ('url_pattern', 'ip_group', 'reverse_ip_group', 'is_allowed', 'move_up_url', 'move_down_url')


class IPRangeForm(forms.ModelForm):
    class Meta:
        model = models.IPRange
        exclude = ()

    def clean(self):
        cleaned_data = super(IPRangeForm, self).clean()
        first_ip = cleaned_data.get('first_ip')
        if first_ip is None:
            # first_ip is Mandatory, so just let the default validator catch this
            return cleaned_data
        version = ipu.get_version(first_ip)
        last_ip = cleaned_data['last_ip']
        cidr = cleaned_data.get('cidr_prefix_length')
        if cidr is not None:
            if version == ipu.IPv4 and not (1 <= cidr <= 31):
                self.add_error('cidr_prefix_length', 'Must be a number between 1 and 31')
                return cleaned_data
            if version == ipu.IPv6 and not (1 <= cidr <= 127):
                self.add_error('cidr_prefix_length', 'Must be a number between 1 and 127')
                return cleaned_data

        if last_ip and cidr:
            raise forms.ValidationError("Don't specify the Last IP if you specified a CIDR prefix length")
        if last_ip:
            if version != ipu.get_version(last_ip):
                raise forms.ValidationError(
                    "Last IP should be the same type as First IP (%s)" % version)
            if ipu.to_number(first_ip) > ipu.to_number(last_ip):
                raise forms.ValidationError("Last IP should be greater than First IP")

        if cidr:
            # With CIDR the starting address could be different than the one
            # the user specified. Making sure it is set to the first ip in the
            # subnet.
            start, end = ipu.cidr_to_range(first_ip, cidr)
            cleaned_data['first_ip'] = ipu.to_ip(start, version=version)

        return cleaned_data


class IPRangeInline(admin.TabularInline):
    model = models.IPRange
    form = IPRangeForm

    fields = ['first_ip', 'cidr_prefix_length', 'last_ip', 'ip_type', 'description']
    readonly_fields = ['ip_type']
    extra = 2


class IPLocationForm(forms.ModelForm):
    class Meta:
        model = models.IPLocation
        exclude = ()

    def clean_country_codes(self):
        codes = self.cleaned_data['country_codes']
        codes = set(filter(lambda x: x != '',
                    NOT_LETTER.split(self.cleaned_data['country_codes'].upper())))

        if not all(map(is_valid_country_code, codes)):
            incorrect = [c for c in codes if not is_valid_country_code(c)]
            msg = ('""%s" must be a valid country code' if len(incorrect) == 1 else
                   '""%s" must be valid country codes')
            raise forms.ValidationError(msg % ', '.join(incorrect))

        codes = list(codes)
        codes.sort()
        return ', '.join(codes)


class IPLocationInline(admin.TabularInline):
    model = models.IPLocation
    form = IPLocationForm

    fields = ['country_codes']
    extra = 2


@admin.register(models.RangeBasedIPGroup)
class RangeBasedIPGroupAdmin(admin.ModelAdmin):
    exclude = ('type',)
    inlines = [IPRangeInline]


@admin.register(models.LocationBasedIPGroup)
class LocationBasedIPGroupAdmin(admin.ModelAdmin):
    exclude = ('type',)
    inlines = [IPLocationInline]
