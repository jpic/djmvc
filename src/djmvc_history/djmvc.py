import djmvc

from .views import LogEntryController

djmvc.site.routes.append(LogEntryController)

