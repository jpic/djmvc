Stage 3 — Override default views
==================================

Goal
----

Replace default views with :py:meth:`~djmvc.clonable.Clonable.clone` and add an
extra update view that edits a single field.

Model
-----

.. literalinclude:: ../../src/djmvc_example/stage3/models.py

Controller and registration
---------------------------

.. literalinclude:: ../../src/djmvc_example/stage3/djmvc.py

``ModelController.routes + [...]`` starts from the default route list and
registers your entries afterward. Routes with the same codename replace the
default — here the cloned :py:class:`~djmvc.views.list.ListView` overrides list,
and :py:class:`CategoryUpdateView` adds a new object-menu action.

The cloned list view sets table columns, filter fields, and page size.
:py:class:`CategoryUpdateView` is a second update route
(`http://localhost:8000/article/<pk>/categoryupdate/ <http://localhost:8000/article/%3Cpk%3E/categoryupdate/>`_) that only exposes the
``category`` field and appears in the object action menu alongside the full
update view.

Try it
------

Visit `http://localhost:8000/article/ <http://localhost:8000/article/>`_. Open an article's detail page — the
object menu shows both **Change Article** and **Change category**.

Tests
-----

`tests/test_stage3.py on GitHub <https://github.com/jpic/djmvc/blob/master/tests/test_stage3.py>`_