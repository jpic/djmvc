Stage 4 — What to explore next
==============================

You now have a working CRUD stack. Optional packages (history, debug, auth) are
described in :doc:`../install`. Here are natural next steps not covered by
dedicated stage apps:

List actions
    Stage 3 shows bulk category update (stage 2 already shows single-row
    category edit). Same pattern for archive, export, or reassign.

Menus and tags
    Tag views with ``navigation``, ``object``, or custom labels. Use
    ``controller.get_tagged_views('object', request=request, object=obj)`` in
    templates (see :doc:`../reference/views`).

Runtime route changes
    After ``site.build()``, swap or remove routes on the live registry
    (``site.routes['list'] = …``, ``del site.routes['delete']``).

Routing debug
    Add ``djmvc_debug`` and browse ``/debug/controller/`` as superuser.

Custom templates
    Set ``default_template_name`` on a cloned view, or add templates under
    ``templates/<controller_codename>/`` (see :py:meth:`~djmvc.views.template.TemplateViewMixin.get_template_names`).

Internationalization
    djmvc ships French translations; wrap user-visible strings in ``gettext``
    when overriding views.