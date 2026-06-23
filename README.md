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
