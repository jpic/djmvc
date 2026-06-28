Stage 2 — Override default views
================================

Goal
----

Replace default views with :py:meth:`~djmvc.clonable.Clonable.clone` and add an
extra update view that edits a single field.

Model
-----

.. literalinclude:: ../../src/djmvc_example/stage2/models.py

Controller and registration
---------------------------

.. literalinclude:: ../../src/djmvc_example/stage2/djmvc.py

The cloned :py:class:`~djmvc.views.list.ListView` sets table columns, filter
fields, and page size. :py:class:`CategoryUpdateView` is a second update route
(``/stage2/<pk>/categoryupdate/``) that only exposes the ``category`` field and
appears in the object action menu alongside the full update view.

Try it
------

Visit ``/stage2/``. Open an article's detail page — the object menu shows both
**Change Article** and **Change category**.

Tests
-----

``tests/test_stage2.py``