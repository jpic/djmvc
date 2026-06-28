Stage 0 — Register a model
==========================

Goal
----

Add a Django model and expose default CRUD routes with a
:py:class:`~djmvc.ModelController` in ``djmvc.py``.

Model
-----

.. literalinclude:: ../../src/djmvc_example/stage0/models.py

Controller and registration
---------------------------

Create ``yourapp/djmvc.py``, add ``yourapp`` to ``INSTALLED_APPS``, and append
your controller to the site:

.. literalinclude:: ../../src/djmvc_example/stage0/djmvc.py

That is all the routing you need in the app. djmvc autodiscovers ``djmvc.py``
modules and registers list, create, detail, update, delete, and bulk-delete
views with Bulma templates.

After ``migrate``, log in (see :doc:`../install`) and visit
`http://localhost:8000/item/ <http://localhost:8000/item/>`_. URL names look like ``site:item:list``,
``site:item:create``.

.. figure:: /_static/screenshots/item-list.png
   :alt: Default item list with sidebar navigation
   :align: center
   :width: 90%

   Default list view for the ``Item`` model — table, sidebar navigation, and
   create action.

List and detail use Django's ``view`` permission (``view_item``). Create,
update, and delete use ``add``, ``change``, and ``delete``.

.. figure:: /_static/screenshots/success-toast.png
   :alt: Success toast after creating an item
   :align: center
   :width: 90%

   A success toast appears after creating a row.

With ``djmvc_history`` in ``INSTALLED_APPS`` (see :doc:`../install`), every
``ModelController`` also gets a history view at
`http://localhost:8000/item/<pk>/history/ <http://localhost:8000/item/%3Cpk%3E/history/>`_ with no extra code in your
``djmvc.py``.

Select rows on the list to open the built-in bulk-delete action:

.. figure:: /_static/screenshots/bulk-delete-modal.png
   :alt: Bulk delete confirmation modal
   :align: center
   :width: 90%

   Built-in :py:class:`~djmvc.views.delete.DeleteObjectsView` — registered on
   every :py:class:`~djmvc.ModelController` with no extra code.

Tests
-----

`tests/test_stage0.py on GitHub <https://github.com/jpic/djmvc/blob/master/tests/test_stage0.py>`_