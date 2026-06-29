Philosophy
~~~~~~~~~~

**Faster Django development by getting more out of less.** djmvc is not a
parallel web stack — it is a thin MVC layer on top of Django that removes
repetitive wiring while keeping Django's models, permissions, and generic views.

Structure is code, not configuration
====================================

Routing is declared by **nesting controllers and views**, not by hand-editing
``urls.py`` for every endpoint. A :py:class:`~djmvc.ModelController` on a model
gives you list, detail, create, update, delete, and bulk delete. URL segments,
names, and nesting follow from class names and conventions.

Each app appends controllers to :data:`djmvc.site` in ``djmvc.py`` (``site.routes.append(...)``).
:py:meth:`~djmvc.Site.build` autodiscovers those modules — the same “drop a
module in each app” pattern as Django admin's ``admin.py``.

Sane defaults, surgical overrides
=================================

Defaults should work on day one. Customization should be **local and explicit**:

- Replace a default view by registering another route with the **same codename**
- Extend with ``ModelController.routes + [MyView]``
- Tweak at runtime: ``site.routes['delete'] = MyDelete.clone(...)``
- Use :py:meth:`~djmvc.clonable.Clonable.clone` to specialize without new
  module-level classes

The :doc:`registry <reference/registry>` is an ordered override table, not a
pile of magic.

The view *is* the template API
==============================

.. epigraph::

   Ain't no way I'm defining ``get_context_data`` for everything.

Add a method or property on the view → use ``{{ view.something }}`` in the
template. :py:class:`~djmvc.views.template.TemplateMixin` puts ``view`` in
context by default. Template logic stays on the view class, not scattered
across context dicts and one-off template tags.

Template power without template-tag sprawl
==========================================

.. epigraph::

   Ain't no way I'm defining a templatetag for everything.

Django templates get Jinja-like freedom via ``{% eval %}`` (see
:doc:`reference/templatetags`), plus filters like ``html_attributes`` and
``unpoly_attributes``. Call view methods from templates; render attribute dicts
without bespoke tags for every case.

Security and data scope in one place
====================================

**Secure by default.** Views check permissions before dispatch; anonymous users
go to login; denied users get 403. CRUD maps to Django's ``add`` / ``change`` /
``delete`` / ``view_<model>`` permissions.

Policy concentrates on the **model controller**:

- :py:meth:`~djmvc.ModelController.has_permission` — who can do what
- :py:meth:`~djmvc.ModelController.get_queryset` — what rows exist for this user

If you already use ``django.contrib.auth.Permission``, you are in familiar
territory — the same model as the admin. Users with ``view_<model>`` can list
and open every row; ``add`` / ``change`` / ``delete`` gate writes. Groups and
per-user permission assignments in the database decide who gets which codename.
That is secure by default: permissions can come from the database already.

In practice, this is fine until you need per-object permissions. So, the first
customization is usually :py:meth:`~djmvc.ModelController.get_queryset`, the
djmvc analogue of ``ModelAdmin.get_queryset`` — filter rows by tenant, owner,
or role while leaving permission checks on the default path. That is enough for
most apps.  When you need **per-object** rules (this user may change *this*
document but not another), override
:py:meth:`~djmvc.ModelController.has_permission` on the controller or
:py:meth:`~djmvc.view.ViewMixin.has_permission` on individual views — the same
escape hatch Django's permission backends provide.

Lists, object views, and bulk actions all share that queryset. PKs outside it →
404, not a leak.

Menus are introspected, not hardcoded
=====================================

Views carry **``tags``** (``topbar``, ``object``, ``list_action``, …).
Controllers expose :py:meth:`~djmvc.controller.Controller.get_tagged_views`,
which instantiates each candidate, runs :py:meth:`~djmvc.view.ViewMixin.has_permission`,
and returns only what the current user (and object, if any) may see.

Navigation is **derived from the route tree**, not duplicated in every template.

.. figure:: /_static/screenshots/item-list.png
   :alt: Sidebar navigation built from tagged list views
   :align: center
   :width: 90%

   Sidebar entries come from views tagged ``navigation``; controller ``icon``
   attributes render beside each label.

Composition over monoliths
==========================

Generic views are **stacks of small mixins** — one concern each (filter,
pagination, tables2, form, object, delete, list_action, …). Override mixin
**attributes** on a subclass or clone; templates read them from ``view``.

:doc:`tutorial/stage5` is the manifesto: understand the mixins, understand the
whole system. See :doc:`reference/mixins/index` for each mixin.

Django all the way down
=======================

djmvc embraces Django rather than fighting it:

- ``user.has_perm()`` and custom backends (crudlfap lineage)
- Django generic views and ``urlpatterns``
- Bulma templates that are **simple enough to copy and adapt** — reference UI,
  not a locked theme

Optional packages (``djmvc_auth``, ``djmvc_history``, ``djmvc_debug``) plug in
the same way: add to ``INSTALLED_APPS``, routes appear. See :doc:`install`.

Progressive complexity
======================

The :doc:`tutorial/index` mirrors how you would actually adopt djmvc:

.. list-table::
   :header-rows: 1
   :widths: 10 90

   * - Stage
     - Idea
   * - 0
     - One model → full CRUD
   * - 1
     - Nest under an app controller
   * - 2
     - Custom non-CRUD views
   * - 3
     - Clone and replace defaults
   * - 4
     - List actions + i18n
   * - 5
     - Mixin tour

Each stage is a working app, literal-included in the docs, validated by
``pytest -m tutorial``.

In one sentence
===============

**Declare a tree of controllers and views, inherit secure CRUD and routing,
expose the view object to templates, and override only what you need — policy
once on the controller, presentation through composable mixins and introspected
menus.**

That is the voice behind “Get more out of less” and the README's informal
“ain't no way I'm…” lines: less boilerplate, fewer files, same Django
underneath.