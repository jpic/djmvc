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

Add these Django apps to ``INSTALLED_APPS``. Each app (and optional package)
appends its controllers to :data:`djmvc.site` in ``djmvc.py``::

    djmvc.site.routes.append(MyController)

:py:meth:`~djmvc.Site.build` imports those modules via autodiscovery — the same
pattern as Django admin's ``admin.py``. The append runs on import, before the
route registry is built.

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
    permission defaults (views redirect anonymous users to login). Includes
    ``Group`` CRUD at ``/auth/group/``.

``djmvc_dal`` (recommended)
    Zero-config autocomplete for relation fields — see
    :ref:`install-djmvc-dal` below. Requires ``dal`` and ``dal_alight``
    **before** ``django.contrib.admin`` in ``INSTALLED_APPS``.

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
       "dal",
       "dal_alight",
       "django.contrib.admin",
       "django.contrib.auth",
       "django.contrib.contenttypes",
       "django.contrib.sessions",
       "django.contrib.messages",
       "django.contrib.staticfiles",
       "djmvc",
       "djmvc_dal",
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

.. _install-djmvc-dal:

djmvc_dal — autocomplete for relation fields
==============================================

``djmvc_dal`` connects `django-autocomplete-light
<https://django-autocomplete-light.readthedocs.io/>`_ (DAL) Alight widgets to
djmvc's controller tree. When a :class:`~djmvc.ModelController` exists for a
related model, every ``ForeignKey``, ``OneToOneField``, and ``ManyToManyField``
on your project automatically gets a searchable autocomplete — in model forms,
in list-filter bars, and anywhere else Django calls ``ModelField.formfield()``.

No per-field widget configuration, no hard-coded autocomplete URLs, and no
build-time URL registry.

What you get
------------

* An :class:`~djmvc_dal.views.AutocompleteView` route on every
  :class:`~djmvc.ModelController` (for example ``/auth/group/autocomplete/``).
* Alight web-component widgets on relation fields whose related model has a
  controller with that autocomplete route.
* The same widgets in :class:`~djmvc.views.filter.FilterMixin` filter bars when
  you set :attr:`~djmvc.views.filter.FilterMixin.filter_fields` (for example
  ``filter_fields=['groups']`` on the user list).
* Form media that survives Unpoly fragment swaps and modal layers (see below).

The example project demonstrates this with ``djmvc_auth``: ``Group`` has a
controller at ``/auth/group/``, and the user list filters by group with an
autocomplete in the horizontal search bar.

How it works
------------

``djmvc_dal`` does four things at startup, in order:

1. **Register an autocomplete route on every model controller.**
   Importing :mod:`djmvc_dal.models` appends
   :class:`~djmvc_dal.views.AutocompleteView` to
   :attr:`~djmvc.ModelController.routes`. Each controller that passes the usual
   view permission checks exposes ``…/autocomplete/`` for its queryset.

2. **Register a djhacker callback for relation field types.**
   On ``ForeignKey``, ``OneToOneField``, and ``ManyToManyField``,
   :func:`djhacker.register` supplies a callback that builds a
   ``ModelAlight`` / ``ModelAlightMultiple`` widget when an autocomplete URL
   can be resolved for the related model.

3. **Patch every relation field after the site is built.**
   :py:meth:`~djmvc.Site.build` is wrapped so that, once the full controller
   tree exists, :func:`~djmvc_dal.hooks.patch_relation_formfields` walks every
   model and calls :func:`djhacker.formfield` on each relation accessor. From
   that point on, ``YourModel._meta.get_field('groups').formfield()`` returns
   the Alight widget — including for Django's built-in ``UserChangeForm`` and
   for django-filter fields that django-filter would otherwise render as plain
   ``<select>`` elements.

4. **Resolve autocomplete URLs at runtime.**
   :func:`~djmvc_dal.lookup.find_autocomplete_url` walks the built
   :data:`djmvc.site` tree and returns the ``urlfullname`` of the matching
   controller's ``autocomplete`` route. There is no separate registry: if you
   add a :class:`~djmvc.ModelController` for a model, its relation fields start
   autocompleteing automatically.

Search fields on the autocomplete endpoint come from the controller's list view:
:class:`~djmvc_dal.views.AutocompleteView` delegates to
:attr:`~djmvc.views.search.SearchMixin.search_fields` on the list route (CharField
and TextField columns by default). Override ``search_fields`` on a cloned list
view to change what the autocomplete searches.

List filters reuse the same widgets. :class:`~djmvc.views.filter.FilterMixin`
calls :meth:`~django.db.models.Field.formfield` and copies the patched widget
onto the django-filter form field, so ``filter_fields=['groups']`` renders the
same Alight control as the user update form.

Unpoly, modals, and ``form.media``
-----------------------------------

Unpoly modal fragments swap body content only — ``{% block extra_js %}`` in the
page layout is not re-evaluated. djmvc_bulma therefore inlines ``{{ form.media
}}`` in form templates (model forms and the horizontal filter bar) so scripts
and styles travel with the fragment.

DAL loads its JavaScript as ES modules (``Script(…, type='module')`` in
``dal_alight``). Browsers evaluate a module script once per URL; when Unpoly
re-inserts the same ``<script type="module" src="…">`` tag after a filter
submit or modal open, the custom elements and adapters do not re-initialize.
That is what makes inline ``form.media`` safe here.

Requirements
------------

* ``dal`` and ``dal_alight`` in ``INSTALLED_APPS`` **before**
  ``django.contrib.admin`` (DAL's own requirement).
* ``djmvc_dal`` after ``djmvc`` (it patches :class:`~djmvc.ModelController` and
  :class:`~djmvc.Site`).
* ``djhacker`` — installed as a core dependency of ``djmvc``; ``djmvc_dal`` uses
  it to patch ``formfield()`` on relation fields project-wide.

API reference: :doc:`reference/djmvc_dal/index`.

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