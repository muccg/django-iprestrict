# -*- coding: utf-8 -*-
'''Client-side wrapper lib around GeoIP.

By using this module we allow:
    - if GeoIP2 is unavailable (pre Django 1.9) fall back on GeoIP
    - make the geoip module optional. If the user opts out we don't fail on importing required modules
'''
from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

available_geoip = 2
try:
    from django.contrib.gis.geoip2 import GeoIP2
    from geoip2.errors import AddressNotFoundError
except ImportError:
    available_geoip = 1
    try:
        from django.contrib.gis.geoip import GeoIP
    except ImportError:
        available_geoip = None
try:
    from pycountry import countries
except ImportError:
    if getattr(settings, 'IPRESTRICT_GEOIP_ENABLED', True):
        raise ImproperlyConfigured(
            "You are using location based IP Groups, but the python package "
            "pycountry isn't installed. Please install pycountry or set 'IPRESTRICT_GEOIP_ENABLED' "
            "to False in settings.py")


# Special value for IP addresses that have no country like localhost.
# Using the 'XX' special value allows for rules being set up on the 'XX' country code
# and giving more control to end-users on what to do for special cases like this
NO_COUNTRY = 'XX'


class AdaptedGeoIP2(object):
    '''Makes GeoIP2 behave like GeoIP'''
    def __init__(self, *args, **kwargs):
        self._geoip = GeoIP2()

    def country_code(self, ip):
        # if the IP isn't in the DB return None instead of throwing an Exception as GeoIP does
        try:
            return self._geoip.country_code(ip)
        except AddressNotFoundError:
            return None


class OurGeoIP(object):

    def country_code(self, ip):
        raise ImproperlyConfigured(
            "You are using location based IP Groups, "
            "but 'IPRESTRICT_GEOIP_ENABLED' isn't set to True in settings.py")


_geoip = OurGeoIP()
if getattr(settings, 'IPRESTRICT_GEOIP_ENABLED', True):
    if available_geoip is None:
        raise ImproperlyConfigured(
            "'IPRESTRICT_GEOIP_ENABLED' is set to True, but neither geoip nor geoip2 is available "
            " to import. Make sure the geoip libraries are installed as described in the Django "
            "documentation")
    _geoip = AdaptedGeoIP2() if available_geoip == 2 else GeoIP()


def get_geoip():
    return _geoip


def is_valid_country_code(code):
    if code == NO_COUNTRY:
        return True
    try:
        countries.get(alpha_2=code)
        return True
    except KeyError:
        return False
