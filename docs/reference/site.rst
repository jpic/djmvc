ModelController and site
~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: djmvc.ModelController
   :members:
   :show-inheritance:

.. autoclass:: djmvc.Site
   :members:
   :show-inheritance:

.. autoclass:: djmvc.Home
   :members:
   :show-inheritance:

.. data:: djmvc.site

   Root :class:`~djmvc.Site` instance. Before :meth:`~djmvc.Site.build`,
   ``site.routes`` is the declaration list — append controllers from each app's
   ``djmvc.py`` with ``site.routes.append(...)`` (see :doc:`../tutorial/stage0`).
   Call ``djmvc.site.build()`` from your project's ``urls.py`` to autodiscover
   those modules and obtain ``urlpatterns``.