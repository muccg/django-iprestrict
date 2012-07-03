from iprestrict import models
from django.contrib import admin


#class ChoiceInline(admin.TabularInline):
#    model = Choice
#    extra = 3

#class PollAdmin(admin.ModelAdmin):
#    fieldsets = [
#        (None,               {'fields': ['question']}),
#        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
#    ]
#    inlines = [ChoiceInline]
#    list_display = ('question', 'pub_date', 'was_published_recently')
#    list_filter = ['pub_date']
#    search_fields = ['question']
#    date_hierarchy = 'pub_date'
#
#admin.site.register(Poll, PollAdmin)

class RuleAdmin(admin.ModelAdmin):
    model = models.Rule

    list_display = ('url_pattern', 'ip_group', 'is_allowed')


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

