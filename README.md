# Faster Django development

Get more out of less with a few design patterns:

- MVC to skip manual URL Routing definition and menu generation
- Skip `get_context_data` overrides by consuming the `view` object directly in
  templates
- `{% eval %}` template tag to skip making template tags every time you want to
  call a function or method (like in Jinja2)

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
