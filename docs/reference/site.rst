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

   Root :class:`~djmvc.Site` instance. Append controllers in each app's
   ``djmvc.py`` with ``djmvc.site.routes.append(...)``, then include
   ``djmvc.site.build().urlpatterns`` in your project's ``urls.py``.