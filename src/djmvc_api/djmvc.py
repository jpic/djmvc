import djmvc

from .views import ApiController

djmvc.site.routes.append(ApiController)