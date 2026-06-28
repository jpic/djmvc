Stage 5 — View mixins
=====================

djmvc builds each generic view from **mixins** — small classes that add one
concern (filtering, pagination, tables, forms, …). Override mixin
**attributes** on a cloned view or subclass; templates read them from the
``view`` object in context.

See :doc:`../reference/mixins` for every mixin and overridable attribute. Generic
views that combine them are listed under :doc:`../reference/views/index`.

For screenshots of list, filter, pagination, and object-menu mixins in action,
see :doc:`stage3`.

List display
    :py:class:`~djmvc.views.list.ListMixin` —
    :attr:`~djmvc.views.list.ListMixin.default_template_name`,
    :attr:`~djmvc.views.list.ListMixin.tags`,
    :attr:`~djmvc.views.list.ListMixin.permission_shortcode`,
    :attr:`~djmvc.views.list.ListMixin.empty_list_message`

    :py:class:`~djmvc.views.search.SearchMixin` —
    :attr:`~djmvc.views.search.SearchMixin.search_param`,
    :attr:`~djmvc.views.search.SearchMixin.search_fields`

    :py:class:`~djmvc.views.filter.FilterMixin` —
    :attr:`~djmvc.views.filter.FilterMixin.filter_fields`,
    :attr:`~djmvc.views.filter.FilterMixin.filter_form_class`,
    :attr:`~djmvc.views.filter.FilterMixin.filter_target`

    :py:class:`~djmvc.views.pagination.PaginationMixin` —
    :attr:`~djmvc.views.pagination.PaginationMixin.paginate_by`,
    :attr:`~djmvc.views.pagination.PaginationMixin.per_page_options`,
    :attr:`~djmvc.views.pagination.PaginationMixin.page_kwarg`,
    :attr:`~djmvc.views.pagination.PaginationMixin.per_page_kwarg`,
    :attr:`~djmvc.views.pagination.PaginationMixin.pagination_target`

    :py:class:`~djmvc.views.tables2.Tables2Mixin` —
    :attr:`~djmvc.views.tables2.Tables2Mixin.table_template`,
    :attr:`~djmvc.views.tables2.Tables2Mixin.table_fields`

Forms and objects
    :py:class:`~djmvc.views.form.FormMixin` —
    :attr:`~djmvc.views.form.FormMixin.default_template_name`,
    :attr:`~djmvc.views.form.FormMixin.form_attributes`

    :py:class:`~djmvc.views.object.ObjectMixin` — object detail URLs and
    breadcrumbs (see :doc:`../reference/mixins/object`)

    :py:class:`~djmvc.views.modelform.ModelFormMixin` — model forms for
    create/update

    :py:class:`~djmvc.views.delete.DeleteMixin` —
    :attr:`~djmvc.views.delete.DeleteMixin.default_template_name`,
    :attr:`~djmvc.views.delete.DeleteMixin.icon`,
    :attr:`~djmvc.views.delete.DeleteMixin.color`

List actions and permissions
    :py:class:`~djmvc.views.list_action.ListActionMixin` — bulk actions from the
    list action bar (stage 4)

    :py:class:`~djmvc.views.action.ActionMixin` — per-object permission checks
    on delete/update

    :py:class:`~djmvc.view.ViewMixin` —
    :attr:`~djmvc.view.ViewMixin.permission_shortcode`

Templates and model binding
    :py:class:`~djmvc.views.template.TemplateViewMixin` —
    :attr:`~djmvc.views.template.TemplateMixin.default_template_name` via
    ``default_template_name`` on concrete views

    :py:class:`~djmvc.model.ModelMixin` — resolves ``model`` from the enclosing
    :py:class:`~djmvc.ModelController`

    :py:class:`~djmvc.views.log.LogMixin` — audit logging when
    ``djmvc_history`` is installed

Further topics
--------------

Optional packages (history, debug, auth) are described in :doc:`../install`.

Menus and tags
    Tag views with ``navigation``, ``object``, or ``list_action``. Use
    ``controller.get_tagged_views('object', request=request, object=obj)`` in
    templates.

Runtime route changes
    After ``site.build()``, swap or remove routes on the live registry
    (``site.routes['list'] = …``, ``del site.routes['delete']``).

Routing debug
    Add ``djmvc_debug`` and browse `http://localhost:8000/debug/controller/ <http://localhost:8000/debug/controller/>`_ as
    superuser.

Internationalization
    djmvc ships French translations; wrap user-visible strings in ``gettext``
    when overriding views (stage 4).