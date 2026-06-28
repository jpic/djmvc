Stage 4 — Custom list actions
=============================

Goal
----

Add a bulk action on the list view: select rows, pick a new category, apply to
all. Built-in bulk delete (from stage 0) works the same way — subclass
:py:class:`~djmvc.views.list_action.ListActionView`, tag it ``list_action``, and
append it to the controller ``routes``.

Model
-----

.. literalinclude:: ../../src/djmvc_example/stage4/models.py

Controller and registration
---------------------------

.. literalinclude:: ../../src/djmvc_example/stage4/djmvc.py

:py:class:`SetCategoryView` receives selected primary keys as ``pks`` (query
string from the list action bar). ``object_list`` is the scoped queryset
intersection. ``form_valid`` runs your bulk logic — here a single
``QuerySet.update``.

User-visible strings use ``gettext`` and ``ngettext`` so success messages
pluralize correctly.

The list template discovers permitted actions as ``view.list_actions`` and
renders them in ``<list-action-bar>`` next to the default delete action.

Try it
------

Visit `http://localhost:8000/post/ <http://localhost:8000/post/>`_, create a few
posts, select rows, and click **Set category**:

.. figure:: /_static/screenshots/list-action-bar.png
   :alt: List action bar with row selection
   :align: center
   :width: 90%

   Selected rows open the floating ``<list-action-bar>`` with permitted bulk
   actions.

.. figure:: /_static/screenshots/set-category-modal.png
   :alt: Set category bulk action modal
   :align: center
   :width: 90%

   Custom :py:class:`SetCategoryView` — same pattern as the built-in bulk
   delete shown in :doc:`stage0`.

Tests
-----

`tests/test_stage4.py on GitHub <https://github.com/jpic/djmvc/blob/master/tests/test_stage4.py>`_

Next: :doc:`stage5` surveys the view mixins you can combine when building custom
views.