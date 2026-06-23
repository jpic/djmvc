from djmvc.controller import Controller
from djmvc.view import View


# definition by sub-class
class SubController(Controller):
    name = 'sub-controller'
    routes = [
        # definition on-the-fly with clone
        View.clone(
            name='sub-view',
        ),
        Controller.clone(
            name='sub-sub-controller',
            routes=[
                View.clone(
                    name='sub-sub-view',
                )
            ]
        )
    ]


# defining a root controller
Site = Controller.clone(
    name='controller',
    routes=[
        View.clone(
            name='view',
        ),
        SubController,
    ]
)

# and urlpatterns to include
urlpatterns = Site().urlpatterns
