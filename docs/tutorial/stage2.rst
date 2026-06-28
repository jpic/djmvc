Stage 2 — Querysets and permissions
=====================================

Goal
----

Scope which rows a user can reach with
:py:meth:`~djmvc.ModelController.get_queryset`. List and detail already use
Django's ``view`` permission by default (stage 0).

Model
-----

.. literalinclude:: ../../src/djmvc_example/stage2/models.py

Controller and registration
---------------------------

.. literalinclude:: ../../src/djmvc_example/stage2/djmvc.py

``get_queryset`` limits non-superusers to documents they own. Grant
``view_document`` for read access; ``delete_document`` for bulk delete on owned
rows.

Try it
------

Visit `http://localhost:8000/document/ <http://localhost:8000/document/>`_. Create two users and documents with
different owners. Each user sees only their rows; detail and bulk delete ignore
out-of-scope primary keys.

Tests
-----

`tests/test_stage2.py on GitHub <https://github.com/jpic/djmvc/blob/master/tests/test_stage2.py>`_