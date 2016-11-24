Changing and reloading rules
============================

.. _rules-are-cached:

Rules are cached
----------------

In order to avoid the reload of rules on each request the rules are cached on the first load from the middleware.
This also means that if the rule are changed they have to be re-loaded somehow into the middleware.

One possibility is to just restart your server after you change the rules.
In case this is acceptable for you just set the following variable into your settings file::

  IPRESTRICT_RELOAD_RULES = False

The second possibility (which is the default behaviour) is to request a rule reload. The next time the middleware will receive a request the rules will be reloaded. There is a custom management command for reloading rules::

  $ ./manage.py reload_rules

The advantage of this approach is that you don't have to restart your server every time you change your rules.
The disadvantage is that on each request a query will be executed that selects the first row from the ``reloadrulesrequest`` DB table.


Changing the rules on a production server
-----------------------------------------

In case you are using the default caching described above, remember that every time you change your rules you will have to follow up with running the ``reload_rules`` command.

However, the recommended way of changing your restriction rules is to make the changes using admin on a staging server and test them there, export them and then import them on the production server instead of changing rules directly on the production server. 

After you changed the rules and are happy with them you can export them using::

  $ ./manage.py dumpdata iprestrict --indent=4 --exclude iprestrict.ReloadRulesRequest > new_rules.json

Then you can copy the new_rules.json file to your production server and import them with the custom management command ``import_rules``. For example if you've copied your rules file to ``/tmp`` you would use::

  $ ./manage.py import_rules /tmp/new_rules.json

You would also have to reload the rules or restart the server (depending on what caching strategy you are using)::

  $ ./manage.py reload_rules

