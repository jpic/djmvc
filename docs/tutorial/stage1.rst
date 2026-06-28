Stage 1 — Querysets and permissions
=====================================

Goal
----

Scope which rows a user can reach with
:py:meth:`~djmvc.ModelController.get_queryset`, then open list and detail to
non-superusers with Django's ``view`` permission.

Model
-----

.. literalinclude:: ../../src/djmvc_example/stage1/models.py

Controller and registration
---------------------------

.. literalinclude:: ../../src/djmvc_example/stage1/djmvc.py

``get_queryset`` limits non-superusers to documents they own. List and detail
use ``permission_shortcode='view'`` so granting ``view_document`` is enough for
read access. ``has_permission`` delegates view checks to Django's permission
backend.

Try it
------

Visit ``/stage1/``. Create two users and documents with different owners. Each
user sees only their rows; detail and bulk delete ignore out-of-scope PKs.

Tests
-----

``tests/test_stage1.py``