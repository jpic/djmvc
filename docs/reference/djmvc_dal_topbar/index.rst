djmvc_dal_topbar
~~~~~~~~~~~~~~~~

.. automodule:: djmvc_dal_topbar.views
   :members:
   :show-inheritance:

.. automodule:: djmvc_dal_topbar.lookup
   :members:
   :show-inheritance:

Site search
-----------

:class:`~djmvc_dal_topbar.views.SiteSearchView` is registered on :data:`djmvc.site` at
``/search/``. Discovery helpers in :mod:`djmvc_dal_topbar.lookup` walk model
controllers and yield list views the user may search. The navbar partial is
:file:`djmvc_dal_topbar/templates/djmvc/_site_search.html`.