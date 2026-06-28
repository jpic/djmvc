import djmvc

from .views import RoutingDebugController

djmvc.site.routes.append(RoutingDebugController)

