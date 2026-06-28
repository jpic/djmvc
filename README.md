# Faster Django development

**Documentation:** https://jpic.github.io/djmvc/

Get more out of less with a few design patterns:

- Skip manual URL routing with MVC pattern and sane defaults
- Dynamic navigation menus with tagged views
- Skip `get_context_data` overrides by consuming the `view` object directly in
  templates
- `{% load djmvc %}` template library (`{% eval %}`, `html_attributes`,
  `unpoly_attributes` filters) to skip boilerplate template tags
- Secure by default: views delegate permissions to the controller, which checks
  Django permissions (`user.has_perm()`). List/detail use custom codenames
  (`view_<model>`) for list and detail; CRUD views
  use Django's built-in `add`/`change`/`delete` permissions.

Install with:

```
pip install djmvc[bulma]
```

## Routing

Skip manual URL routing definition by nesting views and controllers:

```python
import djmvc


class Home(djmvc.TemplateView):
    urlpath = ''
    def your_stuff(self):
        return stuff_for_the_template()


class Site(djmvc.Controller):
    routes=[
        Home,
        # nest a CRUD controller
        djmvc.ModelController(
            model=YourModel,
        ),
    ]

site = Site()

# in your project's urls.py — build discovers per-app djmvc.py modules
urlpatterns = site.build().urlpatterns

# it will define reverseable urls
assert reverse('site:home') == '/'
assert reverse('controller:sub-controller:sub-view') == '/controller/sub-controller/sub-view/'
```

### Per-app route registration

Each installed app can provide a `djmvc.py` module that appends routes
(imported during `site.build()`, same pattern as Django admin's `admin.py`):

```python
# myapp/djmvc.py
import djmvc
from .views import MyController

djmvc.site.routes.append(MyController)
```

Use `reverse_lazy()` for any settings that hold URL names (e.g. `LOGIN_URL`).

### Runtime route customization

`site.build()` clones declared `routes` into a live registry on the instance.
After build, `site.routes` is that registry (class-level `MyController.routes`
stays the declaration list). Customize at runtime:

```python
site.routes.register(Extra)

# swap a whole entry
site.routes['home'] = Dashboard.clone(urlpath='')

# remove a route
del site.routes['delete']
```

### Routing debug UI

Add `djmvc_debug` to `INSTALLED_APPS` for a superuser-only browser UI that
introspects the live route registry:

```python
INSTALLED_APPS += ["djmvc_debug"]
```

Superusers can then browse `/debug/controller/` and `/debug/url/`.

## Templates

Ain't no way I'm defining get_context_data for everything I add to a view, I
consider that adding a method or property to the view should make it directly
accessible from the template, as such, the default TemplateMixin provides a
`get_context_data` which already returns the `view` as context object.

```python
from djmvc.views import generic

class MyView(generic.TemplateView):
    @property
    def something(self):
        return Some.thing()
```

Allows directly that in the template: `{{ view.something }}`.

Also, ain't no way I'm defining a templatetag for everything, loved the liberty
Jinja2 gave me, taking it back with Django engine with the `djmvc` template
library.

```python
class MyView(generic.TemplateView):
    def something(self, some_var, user):
        return Some.thing(some_var, user)
```

Becomes available as:

```jinja2
{% load djmvc %}
{% eval view.some_method "some test var" user=view.request.user as result %}
{{ result }}
```

Form views can define Unpoly link attributes per rendering context (list menu,
table actions, etc.) with `unpoly_attributes(context)` on `FormMixin`. Render
them in templates without hardcoding view names:

```jinja2
{% load djmvc %}
<a href="{{ action.url }}" {{ action|unpoly_attributes:'model_menu'|html_attributes }}>
```

Any attribute dict (forms included) can use the `html_attributes` filter:

```jinja2
<form method="post" {{ view.form_attributes|html_attributes }}>
```

## Permissions and querysets

Views check `has_permission()` before dispatch. By default the call chain is:

```
view.has_permission()
  → controller.has_permission(view)
    → view.has_permission_backend()
      → user.has_perm(permission_fullcode)          # Django model perms
      → user.has_perm(permission_fullcode, view)    # custom backends
```

`has_permission_backend()` tries Django codename permissions first (without
passing the view, because ModelBackend ignores perms when `obj` is set), then
calls again with the view so custom backends can introspect it — same pattern
as crudlfap's `has_perm_backend()`.

Override `has_permission()` to open a view to everyone (`return True`) or
encode custom rules (login pages, per-user checks). CRUD views set
`permission_shortcode` to Django's
`add`, `change`, and `delete`. List and detail default to Django's `view`
permission (`view_<model>`).

Override policy in one place on the model controller:

```python
class YourModelController(djmvc.ModelController):
    model = YourModel

    def has_permission(self, view):
        return view.has_permission_backend()

    def get_queryset(self, view):
        qs = super().get_queryset(view)
        if not self.request.user.is_superuser:
            qs = qs.filter(owner=self.request.user)
        return qs
```

`ModelMixin.get_queryset()` delegates to the controller, so lists, object
views, and bulk actions all respect the same scoped queryset. Object views
return 404 for PKs outside that queryset.

## Dynamic menus

Add any tags you like to your views:

```python
class YourView(generic.TemplateView):
    tags = ['topbar']

    def has_permission(self):
        return self.request.user.is_authenticated
```

And use the `get_tagged_view()` method of the controller to get all views
tagged `"topbar"` as such:

```jinja2
{% load djmvc %}
{% eval view.root_controller.get_tagged_views 'topbar' request=request as topbar_menu %}
```

Here, we're passing the `request` kwarg to `get_tagged_views()` which will
instanciate the view object with passed kwargs and call `has_permission()`
prior to returning the tagged view.

It also works with per-object permissions via `ActionMixin` on update/delete
views:

```python
class YourModelUpdateView(generic.UpdateView):
    def has_permission_object(self):
        return self.object.owner == self.request.user
```

Or override `has_permission()` entirely:

```python
class YourModelDetailView(generic.DetailView):
    tags = ['object']

    def has_permission(self):
        return (
            super().has_permission()
            and self.object.owner == self.request.user
        )
```

Which will make that view show conditionnaly based on the request user, so that
you can get all the views authorized for a user on a given object in the
"object" tag as such:

```jinja2
{% load djmvc %}
{% eval view.root_controller.get_tagged_views 'object' request=request object=object as object_menu %}
```

### List actions

List actions are form views tagged `list_action` that operate on selected table
rows. `ListActionMixin` provides selection plumbing (`pks`, `object_list`,
`invalid_pks`), redirects back to the list on success, and wires Unpoly for the
floating action bar. Your bulk logic goes in `form_valid()`:

```python
import djmvc


class ArchiveObjectsView(djmvc.generic.ListActionView):
    title = 'Archive'
    icon = 'archive'
    color = 'warning'
    message = 'Archive the selected items?'

    def form_valid(self, form):
        self.object_list.update(archived=True)
        return super().form_valid(form)


class YourModelController(djmvc.ModelController):
    model = YourModel
    routes = [
        djmvc.generic.ListView,
        djmvc.generic.DetailView,
        djmvc.generic.UpdateView,
        djmvc.generic.DeleteView,
        djmvc.generic.CreateView,
        ArchiveObjectsView,
    ]
```

Register the view on your controller `routes` — list views discover permitted
actions as `view.list_actions`. The default Bulma `list.html` already renders
`<list-action-bar>` with `unpoly_attributes:'list_action_bar'`; custom list
templates can loop over `view.list_actions` the same way.

Override `has_permission()` on the list action view for per-row checkbox
visibility — same pattern as the `object` tag.

#### Built-in bulk delete

`ModelController` also registers `DeleteObjectsView`, which composes
`DeleteMixin` (cascade preview, `form_delete.html`) with `ListActionMixin`. Use
it as-is, or subclass it if you need custom delete behavior:

```python
class DeleteObjectsView(DeleteMixin, ListActionMixin, FormView):
    def form_valid(self, form):
        if not self.can_confirm_delete:
            return self.form_invalid(form)
        self.object_list.delete()
        return super().form_valid(form)
```
