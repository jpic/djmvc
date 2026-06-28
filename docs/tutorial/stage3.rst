Stage 3 — Custom list actions
=============================

Goal
----

Add a bulk action on the list view: select rows, pick a new category, apply to
all. Built-in bulk delete (from stage 0) works the same way — subclass
:py:class:`~djmvc.views.list_action.ListActionView`, tag it ``list_action``, and
register it on the controller ``routes``.

Model
-----

.. literalinclude:: ../../src/djmvc_example/stage3/models.py

Controller and registration
---------------------------

.. literalinclude:: ../../src/djmvc_example/stage3/djmvc.py

:py:class:`SetCategoryView` receives selected primary keys as ``pks`` (query
string from the list action bar). ``object_list`` is the scoped queryset
intersection. ``form_valid`` runs your bulk logic — here a single
``QuerySet.update``.

The list template discovers permitted actions as ``view.list_actions`` and
renders them in ``<list-action-bar>`` next to the default delete action.

Try it
------

Visit ``/stage3/``, create a few posts, select rows, and click **Set category**.

Tests
-----

``tests/test_stage3.py``