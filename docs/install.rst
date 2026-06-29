Install djmvc
~~~~~~~~~~~~~

Install the package
===================

.. code-block:: bash

   pip install --pre djmvc

This installs djmvc with all runtime dependencies including the Bulma UI framework.

.. note::

   The ``--pre`` flag is required to install pre-release versions of dependencies
   (currently ``django-autocomplete-light>=5.1``).

.. tip::

   Want to try djmvc first? See :doc:`demo` for a quick walkthrough of the example project.

For local development (tests, docs, example project):

.. code-block:: bash

   git clone https://github.com/jpic/djmvc.git
   cd djmvc
   pip install --pre -e ".[dev,docs]"

Create a Django project
========================

.. code-block:: bash

   django-admin startproject myproject
   cd myproject

Configure settings
==================

Import the djmvc apps and add Django's contrib apps:

.. code-block:: python

   # myproject/settings.py
   import djmvc.settings

   INSTALLED_APPS = djmvc.settings.INSTALLED_APPS + [
       "django.contrib.admin",
       "django.contrib.auth",
       "django.contrib.contenttypes",
       "django.contrib.sessions",
       "django.contrib.messages",
       "django.contrib.staticfiles",
       # your apps with a djmvc.py module:
       # "myapp",
   ]

:mod:`djmvc.settings.INSTALLED_APPS` includes djmvc core, Bulma UI, authentication,
autocomplete (DAL), site search, audit logging, and JSON API. The order ensures
``dal`` and ``dal_alight`` load before ``django.contrib.admin``.

Configure middleware for the JSON API:

.. code-block:: python

   # myproject/settings.py
   MIDDLEWARE = [
       "django.middleware.security.SecurityMiddleware",
       "django.contrib.sessions.middleware.SessionMiddleware",
       "djmvc_api.middleware.BearerCsrfMiddleware",        # Before CsrfViewMiddleware
       "django.middleware.locale.LocaleMiddleware",
       "django.middleware.common.CommonMiddleware",
       "django.middleware.csrf.CsrfViewMiddleware",
       "django.contrib.auth.middleware.AuthenticationMiddleware",
       "djmvc_api.middleware.BearerUserMiddleware",         # After AuthenticationMiddleware
       "django.middleware.messages.middleware.MessageMiddleware",
       "django.middleware.clickjacking.XFrameOptionsMiddleware",
   ]

Both Bearer middleware classes are required for API token authentication.

Initialize the database
=======================

.. code-block:: bash

   python manage.py migrate
   python manage.py createsuperuser

Configure URLs
==============

Wire the djmvc site in your project's ``urls.py``:

.. code-block:: python

   # myproject/urls.py
   from django.contrib import admin
   from django.urls import path
   import djmvc

   urlpatterns = djmvc.site.build().urlpatterns + [
       path("admin/", admin.site.urls),
   ]

:py:meth:`~djmvc.Site.build` autodiscovers every installed app's ``djmvc.py``
module and builds the routing tree.

Start developing
================

.. code-block:: bash

   python manage.py runserver

Visit http://localhost:8000/auth/login/ to log in with your superuser credentials.

Next steps
==========

**Tutorial**: Start with :doc:`tutorial/stage0` to create your first model controller.

**Reference documentation**:

* :doc:`reference/djmvc_api/index` — JSON REST API, Bearer tokens, and Swagger UI
* :doc:`reference/djmvc_dal/index` — Autocomplete for relation fields
* :doc:`reference/djmvc_dal_topbar/index` — Site-wide search in the navbar
* :doc:`reference/djmvc_history/index` — Audit logging and history views
* :doc:`reference/djmvc_auth/index` — Authentication views
* :doc:`reference/djmvc_debug/index` — Route introspection (development only)

**Example project**: See the full example project settings at `djmvc_example/settings.py on GitHub <https://github.com/jpic/djmvc/blob/master/src/djmvc_example/settings.py>`_.
