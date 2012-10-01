Configuration
=============

Add ``iprestrict``, ``south`` (if you aren't using south already) and ``templatetag_handlebars`` to ``INSTALLED_APPS`` in your settings file::

  INSTALLED_APPS = (
    ...
    'south',
    'templatetag_handlebars',
    'iprestrict',
  )

In case you didn't had South installed already run ``syncdb`` to create South's database schema.

Run the migrations for the ``iprestrict`` application::

  $ ./manage.py migrate iprestrict

Enable Django Admin for at least the iprestrict application.

Make sure the the egg template loader is enabled in your setting file::

  TEMPLATE_LOADERS = (
    ...
    'django.template.loaders.eggs.Loader',
  )

Add the urls of iprestrict to your project. Ex in your root urls.py::

  from django.conf.urls import patterns, url, include

  urlpatterns = patterns('',
      # ... snip ...
      (r'^iprestrict/', include('iprestrict.urls')),

This configuration should be enough to let you configure and test your restriction rules.

