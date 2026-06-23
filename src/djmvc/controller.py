from django.urls import include, path

from .clonable import Clonable
from .route import Route


class Controller(Clonable, Route):
    @property
    def urlpatterns(self):
        patterns = []

        for route in self.routes:
            patterns += route().urlpatterns

        return [
            path(
                self.urlpath,
                include(
                    (patterns, self.urlname),
                    namespace=self.urlname,
                ),
            )
        ]
