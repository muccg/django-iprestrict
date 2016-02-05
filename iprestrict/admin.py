from django.contrib import admin
from django import forms
from . import ip_utils as ipu
from . import models


class RuleAdmin(admin.ModelAdmin):
    model = models.Rule

    exclude = ('rank',)
    list_display = ('url_pattern', 'ip_group', 'is_allowed', 'move_up_url', 'move_down_url')


class IPRangeForm(forms.ModelForm):
    class Meta:
        model = models.IPRange
        exclude = ()

    def clean_cidr_prefix_length(self):
        cidr = self.cleaned_data['cidr_prefix_length']
        if cidr:
            if not (1 <= cidr <= 31):
                raise forms.ValidationError("Must be a number between 1 and 31")

        return cidr

    def clean(self):
        cleaned_data = super(IPRangeForm, self).clean()
        first_ip = cleaned_data.get('first_ip')
        if first_ip is None:
            # first_ip is Mandatory, so just let the default validator catch this
            return cleaned_data
        last_ip = cleaned_data['last_ip']
        cidr = cleaned_data.get('cidr_prefix_length', None)

        if last_ip and cidr:
            raise forms.ValidationError("Don't specify the Last IP if you specified a CIDR prefix length")
        if last_ip:
            if ipu.get_version(first_ip) != ipu.get_version(last_ip):
                raise forms.ValidationError("Last IP should be the same type as First IP (%s)" % ipu.get_version(first_ip))
            if ipu.get_version(last_ip) != 'ipv6':
                # Ignore rest of validation for ipv6, support isn't there yet
                if ipu.to_number(first_ip) > ipu.to_number(last_ip):
                    raise forms.ValidationError("Last IP should be greater than First IP")

        if cidr:
            # With CIDR the starting address could be different than the one
            # the user specified. Making sure it is set to the first ip in the
            # subnet.
            start, end = ipu.cidr_to_range(first_ip, cidr)
            cleaned_data['first_ip'] = ipu.to_ip(start)

        return cleaned_data


class IPRangeInline(admin.TabularInline):
    model = models.IPRange
    form = IPRangeForm

    fields = ['first_ip', 'cidr_prefix_length', 'last_ip', 'ip_type']
    readonly_fields = ['ip_type']
    extra = 2


class IPGroupAdmin(admin.ModelAdmin):
    model = models.IPGroup
    inlines = [IPRangeInline]


admin.site.register(models.Rule, RuleAdmin)
admin.site.register(models.IPGroup, IPGroupAdmin)
