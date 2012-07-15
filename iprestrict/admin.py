from iprestrict import models
from django.contrib import admin

class RuleAdmin(admin.ModelAdmin):
    model = models.Rule

    list_display = ('url_pattern', 'ip_group', 'is_allowed', 'move_up_url', 'move_down_url')


class IPRangeInline(admin.TabularInline):
    model = models.IPRange
    fields = ['first_ip', 'last_ip', 'ip_type']
    readonly_fields = ['ip_type']
    extra = 2

class IPGroupAdmin(admin.ModelAdmin):
    model = models.IPGroup
    inlines = [IPRangeInline]

admin.site.register(models.Rule, RuleAdmin)
admin.site.register(models.IPGroup, IPGroupAdmin)

