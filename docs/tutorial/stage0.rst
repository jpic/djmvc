Stage 0 — Register a model
==========================

Goal
----

Add a Django model and expose default CRUD routes with a
:py:class:`~djmvc.ModelController` in ``djmvc.py``. Wire the site in
``urls.py``.

Model
-----

.. literalinclude:: ../../src/djmvc_example/stage0/models.py

Controller and registration
-----------------------------

Create ``yourapp/djmvc.py``, add ``yourapp`` to ``INSTALLED_APPS``, and append
your controller to the site:

.. literalinclude:: ../../src/djmvc_example/stage0/djmvc.py

That is all the routing you need in the app. djmvc autodiscovers ``djmvc.py``
modules and registers list, create, detail, update, delete, and bulk-delete
views with Bulma templates.

URLs
----

In your project's ``urls.py``, call :py:meth:`~djmvc.controller.Controller.build`
on the root site:

.. literalinclude:: ../../src/djmvc_example/urls.py

After ``migrate`` and ``createsuperuser``, visit ``/stage0/``. URL names look
like ``site:stage0:list``, ``site:stage0:create``.

By default, list and detail require superuser. Create/update/delete use Django's
``add`` / ``change`` / ``delete`` permissions.

With ``djmvc_history`` in ``INSTALLED_APPS`` (see :doc:`../install`), every
``ModelController`` also gets a history view at ``/stage0/<pk>/history/`` with
no extra code in your ``djmvc.py``.

Tests
-----

``tests/test_stage0.py``