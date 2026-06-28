Install djmvc
~~~~~~~~~~~~~

From PyPI
=========

.. code-block:: bash

   pip install djmvc[bulma]

For local development (tests, docs, example project):

.. code-block:: bash

   git clone https://github.com/jpic/djmvc.git
   cd djmvc
   pip install -e ".[bulma,dev,docs]"

djmvc applications
==================

Add these Django apps to ``INSTALLED_APPS``. Each optional package registers
routes on :data:`djmvc.site` through its own ``djmvc.py`` module (autodiscovered
during :py:meth:`~djmvc.controller.Controller.build`, like Django admin's
``admin.py``).

``djmvc`` (required)
    Core framework: :py:class:`~djmvc.ModelController`, generic CRUD views,
    routing registry, template tags. No UI templates by itself.

``djmvc_bulma`` (recommended)
    Reference UI maintained in this repository: plain Django templates with
    `Bulma <https://bulma.io/>`_. The markup is intentionally simple so you can
    copy and adapt it. Bulma is customizable through `CSS variables
    <https://bulma.io/documentation/customize/with-css-variables/>`_.
    Requires ``crispy_forms``, ``crispy_bulma``, and ``django_tables2``.

``djmvc_auth`` (recommended)
    Login, logout, and user CRUD at ``/auth/``. Mount this if you use djmvc's
    permission defaults (views redirect anonymous users to login).

``djmvc_history`` (optional)
    Patches every :py:class:`~djmvc.ModelController` with a history view and
    registers a global log-entry browser at ``/logentry/``. Uses Django's
    ``LogEntry`` model.

``djmvc_debug`` (optional, development)
    Superuser-only route introspection at ``/debug/controller/`` and
    ``/debug/url/``.

Minimal ``INSTALLED_APPS`` for a new project:

.. code-block:: python

   INSTALLED_APPS = [
       "django.contrib.admin",
       "django.contrib.auth",
       "django.contrib.contenttypes",
       "django.contrib.sessions",
       "django.contrib.messages",
       "django.contrib.staticfiles",
       "djmvc",
       "djmvc_auth",
       "djmvc_bulma",
       "crispy_forms",
       "crispy_bulma",
       "django_tables2",
       # your apps with a djmvc.py module:
       # "myapp",
   ]

The example project adds ``djmvc_history``, ``djmvc_debug``, and tutorial apps
``djmvc_example.stage0`` through ``stage4``.

URL configuration
=================

Wire the site root in ``urls.py`` — :py:meth:`~djmvc.controller.Controller.build`
autodiscovers every installed app's ``djmvc.py`` and returns Django
``urlpatterns``:

.. literalinclude:: ../src/djmvc_example/urls.py

Example project settings
========================

Full settings for the tutorial harness (all optional packages and stage apps):

`djmvc_example/settings.py on GitHub <https://github.com/jpic/djmvc/blob/master/src/djmvc_example/settings.py>`_

Run the example
===============

From the repository root, use :file:`manage.py`:

.. code-block:: bash

   python manage.py migrate
   python manage.py runserver

After ``migrate``, log in as superuser with username ``su`` and password
``su`` (seeded by the example project's data migration) at
`Log in <http://localhost:8000/auth/login/>`_.

Visit `http://localhost:8000/item/ <http://localhost:8000/item/>`_.

.. figure:: /_static/screenshots/item-list.png
   :alt: Item list with sidebar navigation and table
   :align: center
   :width: 90%

   Reference Bulma UI with sidebar navigation after a minimal install.

Continue with the :doc:`tutorial/index`.

Regenerate documentation screenshots
====================================

Screenshots are committed under :file:`docs/_static/screenshots/`. After
changing templates or navigation, refresh them (requires Firefox and geckodriver,
same as the browser tests in CI):

.. code-block:: bash

   pytest tests/test_docs_screenshots.py -n0 --splinter-headless
   make -C docs html

Commit the updated PNGs with your doc changes.