import djmvc

from .views import HistoryView


djmvc.ModelController.routes.append(HistoryView)