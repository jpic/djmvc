Try the demo
~~~~~~~~~~~~

The djmvc repository includes a complete example project with all features enabled.
This is the fastest way to explore djmvc's capabilities.

Clone and install
=================

.. code-block:: bash

   git clone https://github.com/jpic/djmvc.git
   cd djmvc
   pip install --pre -e ".[dev,docs]"

This installs djmvc in development mode with all dependencies. The ``--pre`` flag
is required for pre-release dependency versions.

Run the example project
=======================

The example project lives in ``src/djmvc_example/`` and includes:

* All djmvc apps (auth, API, DAL, history, debug)
* Tutorial example apps (stage0 through stage4)
* Seeded test data with a superuser account

Initialize the database:

.. code-block:: bash

   python manage.py migrate

Start the development server:

.. code-block:: bash

   python manage.py runserver

Log in
======

Visit http://localhost:8000/auth/login/ and log in with the pre-seeded superuser:

* **Username:** ``su``
* **Password:** ``su``

Once logged in, you'll see the Bulma UI with sidebar navigation.

Explore the demo
================

**Model controllers** — Visit http://localhost:8000/item/ to see a default CRUD interface
with list, create, detail, update, and delete views.

**Site search** — Use the search bar in the top navigation to search across all
models (requires ``djmvc_dal_topbar``).

**JSON API** — Visit http://localhost:8000/api/ for the Swagger UI. Test the API
with:

.. code-block:: bash

   # Get a Bearer token
   TOKEN=$(curl -s -X POST http://localhost:8000/api/login/ \
     -H 'Content-Type: application/json' \
     -d '{"username":"su","password":"su"}' | python -c "import sys,json; print(json.load(sys.stdin)['token'])")

   # List items via JSON API
   curl -s http://localhost:8000/item/ \
     -H 'Accept: application/json' \
     -H "Authorization: Bearer $TOKEN"

**Tutorial examples** — The example project includes stage0 through stage4 from
the tutorial. Each stage demonstrates different djmvc features:

* **stage0** — Basic model controller
* **stage1** — Custom views and permissions
* **stage2** — Cloning views and overriding routes
* **stage3** — List actions and bulk operations
* **stage4** — Advanced mixins and customization

**Debug tools** — Visit http://localhost:8000/debug/controller/ (superuser only)
to introspect the routing tree.

**History/Audit logging** — Visit http://localhost:8000/logentry/ to browse the
global audit log (requires ``djmvc_history``).

Next steps
==========

After exploring the demo:

1. Read the :doc:`tutorial/index` to understand how the example apps were built
2. Follow the :doc:`install` guide to create your own project
3. Review the :doc:`reference/index` for detailed API documentation

For development contributions, see :doc:`contributing`.
