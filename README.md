# djmvc

**Faster Django development by getting more out of less.**

djmvc is a thin MVC layer on top of Django. Declare controllers and views in
code, get secure CRUD and routing by default, and expose the view object
directly to templates.

Read the [philosophy](https://jpic.github.io/djmvc/philosophy.html) for the
full rationale.

## Install

```bash
pip install --pre djmvc
```

Note: The `--pre` flag is required for pre-release dependency versions.

See [installation](https://jpic.github.io/djmvc/install.html) for setup, or
try the [demo](https://jpic.github.io/djmvc/demo.html) to explore the example
project.

## Quick start

```python
# myapp/djmvc.py
import djmvc

from .models import YourModel


class YourModelController(djmvc.ModelController):
    model = YourModel


djmvc.site.routes.append(YourModelController)
```

```python
# urls.py
import djmvc

urlpatterns = djmvc.site.build().urlpatterns
```

Add `myapp` to `INSTALLED_APPS`. `build()` autodiscovers each app's `djmvc.py`
(like Django admin) — the import runs `routes.append()` before the route
registry is built.

## Documentation

- [Philosophy](https://jpic.github.io/djmvc/philosophy.html)
- [Install](https://jpic.github.io/djmvc/install.html)
- [Demo](https://jpic.github.io/djmvc/demo.html) — Try the example project
- [Tutorial](https://jpic.github.io/djmvc/tutorial/)
- [Reference](https://jpic.github.io/djmvc/reference/)

## Contributing

See the [contributing guide](https://jpic.github.io/djmvc/contributing.html)
for development setup, running tests, updating documentation screenshots, and
JavaScript conventions. Source: [`docs/contributing.rst`](docs/contributing.rst).

## License

MIT