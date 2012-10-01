.. Django IPRestrict documentation master file, created by
   sphinx-quickstart on Wed Aug 15 11:50:03 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Django IP Restrict
==================

Django IPRestrict is an app + middleware to restrict access to all or sections of a Django project by client IP ranges.

The code is released under BSD license and it is hosted on github at https://github.com/sztamas/django-iprestrict.


Table of Contents
=================

.. toctree::
    :maxdepth: 2

    installation
    configuration




Configuring the restriction rules
---------------------------------

Go to your admin page and open IPRestrict Rules to get a list of your current rules.

The rules consist of:

* an URL pattern - this is regex that will be matched against the URL requested by the client. The value "ALL" is special and it will always match (a tad nicer than .*)
* an IP Group - a named group of IP addresses. Examples would be "localnet", "Trusted net", "Sam's Home IP"etc. or the provided "ALL" and "localhost"
* an Action (labeled "Is allowed?") - what to do if both the client url and the ip match the URL Pattern and the IP Group. Possible values are "ALLOW" and "DENY" to allow or deny the request.

The rules are checked in the order you see them from top to bottom. The url the client requested is matched against the URL Pattern and the client IP address is checked if it is in the IP Group. In the case both conditions are true the processing of rules stop, and the fate of the request is decided based on the Action.

If no rules match the request the request will just fall through (ie it will be allowed).

As you can see after installation 2 rules are provided by default. 

* The first one allows all request from localhost
* The second denies all requests

This is a deny by default strategy, when you will have to create rules for all the IP addresses that can access the application explicitly.

To allow everything by default and specify the IP addresses you would like to deny access simply delete the ALL, ALL, DENY rule.

The order of the rules can be changed by clicking the "Move Up" and "Move Down" links. 

Example config::

  /admin/.* localnet ALLOW
  /admin/.* ALL DENY

These rules would restrict access to admin only from localnet, but allow access to the rest of the application.

Example config 2::

  ALL "Fishy IPs" DENY
  ALL "Trusted Nets" ALLOW
  ALL ALL DENY

App can be used only from "Trusted Nets", but even inside the Trusted Nets there are some IPs you would like to Deny access to (defined in "Fishy IPs").

Sooner or later you will probably have to define some IP Groups (ex. like Trusted Nets above).

IP Groups have a name and an optional longer description and they are defined by a a list of IP Ranges.
IP Ranges can be:

* a single IP address (complete just the First ip field)
* a subnet (complete the First ip field and the CIDR prefix length)
* a range of ip addressess (complete the First ip and the Last ip in the range and leave the Cidfr prefix length empty)

Ex.

+-------------------------------------+-------------+--------------------+--------------+
| Value                               | First ip    | Cidr prefix length | Last ip      |
+=====================================+=============+====================+==============+
| single ip 192.168.1.1               | 192.168.1.1 |                    |              |
+-------------------------------------+-------------+--------------------+--------------+
| subnet 192.168.1.1/24               + 192.168.1.1 | 24                 |              |
+-------------------------------------+-------------+--------------------+--------------+
| ip range 192.168.1.1 - 192.168.1.10 | 192.168.1.1 |                    | 192.168.1.10 |
+-------------------------------------+-------------+--------------------+--------------+

Testing the rules
-----------------

When you are happy with the rules you set up, you might want to test them.

Go to YOUR_URL/iprestrict/ page. You can use the page to enter any URL and IP Address and Test them against the rules in your database. 

Enabling the middleware
-----------------------

Add ``iprestrict.middleware.IPRestrictMiddleware`` to your ``MIDDLEWARE_CLASSES`` in your settings file. Generally, you will want this middleware to run early, before your session, auth etc. middlewares::

  MIDDLEWARE_CLASSES = (
      'django.middleware.common.CommonMiddleware',
      'iprestrict.middleware.IPRestrictMiddleware',
      ...
  )

Your Django project is now restricted based on the rules defined.


.. toctree::
   :maxdepth: 2

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

