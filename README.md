# Faster Django development

Get more out of less with a few design patterns:

- Skip manual URL routing with MVC pattern and sane defaults
- Dynamic navigation menus with tagged views
- Skip `get_context_data` overrides by consuming the `view` object directly in
  templates
- `{% eval %}` template tag to skip making template tags every time you want to
  call a function or method (like in Jinja2)
- Secure by default: views allow only superusers by default, it's up to you to
  open permissions as-needed.

Install with:

```
pip install djmvc[bulma]
```

## Routing

Skip manual URL routing definition by nesting views and controllers:

```python
from djmvc.controller import Controller
from djmvc.view import View


# definition by sub-classing
class SubController(Controller):
    name = 'sub-controller'
    routes = [
        View.clone(
            name='sub-view',
        )
    ]


# or just define by cloning
Site = Controller.clone(
    name='controller',
    routes=[
        View.clone(
            name='view',
        ),
        SubController,
    ]
)

# define some importable url patterns to include
urlpatterns = Site().urlpatterns

# it will define reverseable urls
assert reverse('controller:view') == '/controller/view/'
assert reverse('controller:sub-controller:sub-view') == '/controller/sub-controller/sub-view/'
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
Jinja2 gave me, taking it back with Django engine with the eval tag provided by
djmvc.

```python
class MyView(generic.TemplateView):
    def something(self, some_var, user):
        return Some.thing(some_var, user)
```

Becomes available as:

```jinja2
{% load eval %}
{% eval view.some_method "some test var" view.request.user as result %}
{{ result }}
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
{% eval view.root_controller.get_tagged_views 'object' request=request object=object as object_menu %}
```
