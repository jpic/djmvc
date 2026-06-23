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

Ain't no way I'm defining a templatetag for everything, loved the liberty
Jinja2 gave me, taking it back with Django engine with the eval tag provided by
djmvc:

```jinja2
{% load eval %}
{% eval foo.bar "test" var as result %}
{{ result }}
```
