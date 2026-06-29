djmvc_api
~~~~~~~~~

``djmvc_api`` is an optional package that adds:

* A **JSON API** on the same URLs as the HTML CRUD views (REST verbs, no DRF).
* **Bearer token** authentication (no session cookie, no CSRF on token requests).
* **Swagger 2.0** schema, **Swagger UI**, login, and token management under ``/api/``.

Core JSON handlers live in :mod:`djmvc`; this package adds discovery, schema/UI,
tokens, and auth middleware.

JSON API (core ``djmvc``)
=========================

Every :class:`~djmvc.ModelController` exposes JSON on its existing routes.
HTML behaviour is unchanged.

Content negotiation
-------------------

:class:`~djmvc.view.ViewMixin` checks :func:`~djmvc.views.json.wants_json` in
``dispatch()``:

* **GET / POST** — JSON when ``Accept: application/json`` or
  ``Content-Type: application/json``.
* **PUT / PATCH / DELETE** — always routed to ``json_*`` handlers (HTML only uses
  GET and POST).

REST mapping
------------

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - Operation
     - HTTP method
     - Example (``Item`` model)
   * - List
     - ``GET`` + JSON accept
     - ``GET /item/``
   * - Detail
     - ``GET`` + JSON accept
     - ``GET /item/<pk>/detail/``
   * - Create
     - ``POST`` + JSON body
     - ``POST /item/create/``
   * - Update
     - ``PUT`` or ``PATCH`` + JSON body
     - ``PUT|PATCH /item/<pk>/update/``
   * - Delete
     - ``DELETE``
     - ``DELETE /item/<pk>/delete/``

POST to update or delete URLs with a JSON body returns **405** with an
``allowed_methods`` hint — use the proper verb instead.

Anonymous JSON requests receive **401** with ``{"detail": "Authentication required"}``
(not an HTML login redirect).

Session clients (browser or test client with cookies) still use the session and
must send a CSRF token on mutating requests, same as standard Django.

Routes
======

:mod:`djmvc_api.djmvc` registers a single :class:`~djmvc_api.views.ApiController`
on :data:`djmvc.site`. All package URLs live under ``/api/``:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - URL
     - View
   * - ``/api/``
     - :class:`~djmvc_api.views.SwaggerUIView` — Swagger UI
   * - ``/api/schema/``
     - :class:`~djmvc_api.views.SchemaView` — Swagger 2.0 JSON document
   * - ``/api/login/``
     - :class:`~djmvc_api.views.ApiLoginView` — username/password → 1-hour token
   * - ``/api/token/``
     - :class:`~djmvc_api.views.TokenController` — manage API tokens (HTML + JSON)

Enable the package
==================

Add ``djmvc_api`` to ``INSTALLED_APPS`` and register the Bearer middleware
(**required** for token auth and CSRF exemption):

.. code-block:: python

   MIDDLEWARE = [
       "django.middleware.security.SecurityMiddleware",
       "django.contrib.sessions.middleware.SessionMiddleware",
       "djmvc_api.middleware.BearerCsrfMiddleware",   # before CSRF
       "django.middleware.locale.LocaleMiddleware",
       "django.middleware.common.CommonMiddleware",
       "django.middleware.csrf.CsrfViewMiddleware",
       "django.contrib.auth.middleware.AuthenticationMiddleware",
       "djmvc_api.middleware.BearerUserMiddleware",     # after session auth
       "django.middleware.messages.middleware.MessageMiddleware",
       "django.middleware.clickjacking.XFrameOptionsMiddleware",
   ]

Run migrations after enabling the app:

.. code-block:: bash

   python manage.py migrate

The example project already includes both; see
:file:`src/djmvc_example/settings.py`.

Optional install extra (placeholder for future dependencies):

.. code-block:: bash

   pip install djmvc[api]

Bearer authentication
=====================

How it works
------------

Two middleware classes cooperate (all logic stays in ``djmvc_api``):

1. :class:`~djmvc_api.middleware.BearerCsrfMiddleware` (before
   ``CsrfViewMiddleware``) — if ``Authorization: Bearer <token>`` is valid,
   sets ``request._dont_enforce_csrf_checks`` and stashes the token.
2. :class:`~djmvc_api.middleware.BearerUserMiddleware` (after
   ``AuthenticationMiddleware``) — sets ``request.user`` and ``request.auth``
   from the stashed token.

HTML forms on the same URLs still require CSRF when using session cookies.

Obtaining a token
-----------------

**Quick 1-hour token** — ``POST /api/login/`` with JSON credentials (no CSRF,
no prior session):

.. code-block:: bash

   curl -X POST http://localhost:8000/api/login/ \
     -H 'Content-Type: application/json' \
     -d '{"username": "su", "password": "su"}'

Response:

.. code-block:: json

   {
     "token": "<raw-key-shown-once>",
     "expires": "2026-06-29T14:00:00+00:00",
     "prefix": "AbCdEfGh"
   }

**Named / long-lived token** — log in via HTML, open ``/api/token/create/``, submit
the form (session + CSRF). The raw key is shown once in a success message; only
the ``prefix`` is stored for display in the list.

Using a token
-------------

.. code-block:: bash

   curl http://localhost:8000/item/ \
     -H 'Accept: application/json' \
     -H 'Authorization: Bearer <token>'

Mutating requests (``POST``, ``PUT``, ``PATCH``, ``DELETE``) work without a CSRF
header when the Bearer token is valid.

Token model
-----------

:class:`~djmvc_api.models.Token` stores a SHA-256 hash of the key (never the
plaintext). Fields: ``user``, ``name``, ``prefix``, ``created``, optional
``expires``, ``last_used``.

* Non-superusers see **only their own** tokens (list, detail, delete).
* Superusers see all tokens.
* Django permissions: ``view_token``, ``add_token``, ``delete_token`` (no
  ``change`` — tokens are immutable).
* Revoke via HTML delete or ``DELETE /api/token/<pk>/delete/`` with a Bearer token.

Swagger
=======

* ``GET /api/schema/`` — OpenAPI/Swagger 2.0 JSON listing every JSON-capable
  route (not filtered by the current user's permissions). Bearer auth is
  required to execute protected operations.
* ``GET /api/`` — Swagger UI (vendored static assets). Use **Try it out** on
  ``POST /api/login/`` to obtain a token; Swagger UI stores it automatically
  (``persistAuthorization``) and sends ``Authorization: Bearer …`` on other
  operations. You can also click **Authorize** and paste a token manually.
* CRUD operations document ``BearerAuth`` in ``securityDefinitions``.
* ``POST /api/login/`` is documented without Bearer security (it issues tokens).

Serialization
=============

:class:`~djmvc.ModelController` provides :meth:`~djmvc.ModelController.serialize`
and ``json_fields`` on each controller. Override ``json_fields`` or add
``get_<field>_json`` hooks to control the JSON shape.

API reference (modules)
=======================

.. automodule:: djmvc_api.views
   :members:
   :show-inheritance:

.. automodule:: djmvc_api.models
   :members:
   :show-inheritance:

.. automodule:: djmvc_api.middleware
   :members:
   :show-inheritance: