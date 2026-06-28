Stage 1 — App-level controller
==============================

Goal
----

Group routes under an app prefix with :py:class:`~djmvc.Controller`, the same
pattern as :doc:`../install` describes for ``djmvc_auth``.

Stage 0 appended an :py:class:`~djmvc.ModelController` to
:data:`djmvc.site`. Real apps often wrap one or more model controllers (and
extra views such as login) inside a single app-level controller. ``AuthController``
in ``djmvc_auth`` does exactly that — login/logout views plus a nested user CRUD
controller at `http://localhost:8000/auth/user/ <http://localhost:8000/auth/user/>`_.

Controller and registration
---------------------------

The ``Item`` model lives in stage 0. Stage 1 imports it and nests an
``ItemController`` under ``InventoryController``:

.. literalinclude:: ../../src/djmvc_example/stage1/djmvc.py

.. note::

   ``djmvc.ModelController.clone(model=Item)`` would register the same routes
   without a separate controller class — useful for one-off nesting inside
   ``routes``.

``InventoryController`` maps to the URL prefix ``/inventory/``. The nested
``Item`` model controller adds ``/item/`` below that, so the list view is at
`http://localhost:8000/inventory/item/ <http://localhost:8000/inventory/item/>`_ with URL name ``site:inventory:item:list``.

Try it
------

Visit `http://localhost:8000/inventory/item/ <http://localhost:8000/inventory/item/>`_. Create a few items — they share the
same database table as `http://localhost:8000/item/ <http://localhost:8000/item/>`_ from stage 0, but the URL
namespace is different.

Tests
-----

`tests/test_stage1.py on GitHub <https://github.com/jpic/djmvc/blob/master/tests/test_stage1.py>`_