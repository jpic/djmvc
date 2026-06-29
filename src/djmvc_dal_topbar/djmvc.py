import djmvc

from .views import SiteSearchView

djmvc.site.routes.append(SiteSearchView)