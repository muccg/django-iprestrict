#
# Regular cron jobs for the django-iprestrict package
#
0 4	* * *	root	[ -x /usr/bin/django-iprestrict_maintenance ] && /usr/bin/django-iprestrict_maintenance
