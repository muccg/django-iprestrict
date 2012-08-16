.. Django IPRestrict documentation master file, created by
   sphinx-quickstart on Wed Aug 15 11:50:03 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Django IP Restrict
==================

Django IPRestrict is an app + middleware to restrict access to all or sections of a Django project by client IP ranges.

The code is released under BSD license and it is hosted on github at https://github.com/sztamas/django-iprestrict.

Requirements
============

Runtime
-------

* Django 1.4+
* django-templatetag-handlebars 1.2.0+

Development
-----------

In addition to Runtime requirements above:

* django-discover-runner (for running the unit tests)
* sqlite3 (default) or any other RDBMS supported by Django
* Sphinx

Installation
============

You can pip install using a link from the downloads page:

https://github.com/sztamas/django-iprestrict/downloads

Example for version 0.1::

  $ pip install https://github.com/sztamas/django-iprestrict/downloads/django-iprestrict_0.1.tar.gz 

or download the latest version from the downloads page and easy_install it:

Example for version 0.1::

$ easy_install django_iprestrict_0.1.tar.gz

Install django-templateg-handlebars which is a dependency of Django IPRestrict::

  $ pip install django-templatetag-handlebars

Configuration
=============

Add ``iprestrict`` and ``templatetag_handlebars`` to ``INSTALLED_APPS`` in your settings file::

  INSTALLED_APPS = (
    ...
    'templatetag_handlebars',
    'iprestrict',
  )

Run ``syncdb`` (or do whatever you do to add new tables to your Database) to add the database tables.

Enable Django Admin for at least the iprestrict application.

Add the urls of iprestrict to your project. Ex in your root urls.py::

  from django.conf.urls import patterns, url, include

  urlpatterns = patterns('',
      # ... snip ...
      (r'^iprestrict/', include('iprestrict.urls')),

This configuration should be enough to let you configure and test your restriction rules.

By default, IPRestrict will allow full access to all your URLs from localhost only and it will restrict all access from other IPs. Therefore, if you intend to configure your restriction rules using another IP (not localhost), you should not do the next step until your rules are configured.

Add ``iprestrict.middleware.IPRestrictMiddleware`` to your ``MIDDLEWARE_CLASSES`` in your settings file. Generally, you will want this middleware to run early, before your session, auth etc. middlewares::

  MIDDLEWARE_CLASSES = (
      'django.middleware.common.CommonMiddleware',
      'iprestrict.middleware.IPRestrictMiddleware',
      ...
  )


.. toctree::
   :maxdepth: 2

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

