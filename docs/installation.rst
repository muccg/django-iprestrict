Requirements and Installation
=============================

Requirements
------------

* ``Django 1.8+``
* ``django-templatetag-handlebars 1.3.1+``

Additionally, if you would like to use country based restrictions you will need:

* ``pycountry``
* MaxMind_ ``geoip`` or ``geoip2`` libraries as described in the *Django* documentation. Links below.

.. _MaxMind: https://www.maxmind.com

In case you are on at least *Django 1.9* or newer, you should configure geoip2_, if you are on *Django 1.8* you have to use and configure geoip_.

.. _geoip: https://docs.djangoproject.com/en/1.8/ref/contrib/gis/geoip/
.. _geoip2: https://docs.djangoproject.com/en/1.10/ref/contrib/gis/geoip2/

Installation
------------

You can pip install from PyPI::

    pip install django-iprestrict

The country based lookups are optional, if you need it you can install them with::

    pip install django-iprestrict[geoip]

Development
^^^^^^^^^^^

For development create a ``virtualenv``, activate it and then::

    pip install -e .[geoip,dev]

To run the tests against the *python* and *Django* in your virtualenv::

    ./runtests.sh

To run the tests against all combinations of *python 2*, *python 3*, and supported *Django* versions::

    tox

This will also run *flake8*.
