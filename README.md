## Routing

```python
from djmvc.controller import Controller
from djmvc.view import View


Site = Controller.clone(
    name='controller',
    routes=[
        View.clone(
            name='view',
        ),
        Controller.clone(
            name='sub-controller',
            routes=[
                View.clone(
                    name='sub-view',
                )
            ]
        ),
    ]
)

urlpatterns = Site().urlpatterns

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
