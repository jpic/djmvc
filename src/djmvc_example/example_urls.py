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
        ),
    ]
)

urlpatterns = Site().urlpatterns
