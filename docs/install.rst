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
    Bulma layout, sidebar navigation, tables, filters, toasts, Unpoly
    integration. Requires ``crispy_forms``, ``crispy_bulma``, and
    ``django_tables2``.

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
``djmvc_example.stage0`` through ``stage3``.

URL configuration
=================

Wire the site root in ``urls.py`` — :py:meth:`~djmvc.controller.Controller.build`
autodiscovers every installed app's ``djmvc.py`` and returns Django
``urlpatterns``:

.. literalinclude:: ../src/djmvc_example/urls.py

Example project settings
========================

Full settings for the tutorial harness (all optional packages and stage apps):

.. literalinclude:: ../src/djmvc_example/settings.py

Run the example
===============

.. code-block:: bash

   cd src/djmvc_example
   python -m django migrate
   python -m django createsuperuser
   python -m django runserver

Visit ``http://127.0.0.1:8000/stage0/`` after logging in as superuser.

Continue with the :doc:`tutorial/index`.