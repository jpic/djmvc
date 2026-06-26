# Faster Django development

Get more out of less with a few design patterns:

- Skip manual URL routing with MVC pattern and sane defaults
- Dynamic navigation menus with tagged views
- Skip `get_context_data` overrides by consuming the `view` object directly in
  templates
- `{% load djmvc %}` template library (`{% eval %}`, `html_attributes`,
  `unpoly_attributes` filters) to skip boilerplate template tags
- Secure by default: views allow only superusers by default, it's up to you to
  open permissions as-needed.

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

# in your project's urls.py — discover per-app djmvc.py modules first
site.autodiscover()
urlpatterns = site.urlpatterns

# it will define reverseable urls
assert reverse('site:home') == '/'
assert reverse('controller:sub-controller:sub-view') == '/controller/sub-controller/sub-view/'
```

### Per-app route registration

Each installed app can provide a `djmvc.py` module that registers routes
(imported by `site.autodiscover()`, same pattern as Django admin's `admin.py`):

```python
# myapp/djmvc.py
import djmvc
from .views import MyController

djmvc.site.routes.register(MyController)
```

Use `reverse_lazy()` for any settings that hold URL names (e.g. `LOGIN_URL`).

### Runtime route customization

`djmvc.site.routes` is a `Registry` — routes declared on the class are cloned
into it at access time. You can customize it at runtime:

```python
djmvc.site.routes.register(AuthController())

# swap a whole entry
djmvc.site.routes['home'] = Dashboard.clone(urlpath='')

# remove a route
del djmvc.site.routes['delete']
```

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

## Dynamic menus

Add any tags you like to your views:

```python
class YourView(generic.TemplateView):
    tags = ['topbar']

    def has_permission(self):
        return self.request.user.is_authenticated  # the default
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

It also works with per-object permissions as such:

```python
class YourModelDetailView(generic.DetailView):
    tags = ['object']

    def has_permission(self):
        return (
            self.request.user.is_superuser
            or self.object.owner == self.request.user
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
