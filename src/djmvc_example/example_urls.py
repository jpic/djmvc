import djmvc


# definition by sub-class
class SubController(djmvc.Controller):
    codename = 'sub-controller'
    routes = [
        # definition on-the-fly with clone
        djmvc.View.clone(
            codename='sub-view',
        ),
        djmvc.Controller.clone(
            codename='sub-sub-controller',
            routes=[
                djmvc.View.clone(
                    codename='sub-sub-view',
                )
            ]
        )
    ]


# defining a root controller
Site = djmvc.Controller.clone(
    codename='controller',
    routes=[
        djmvc.View.clone(
            codename='view',
        ),
        SubController,
    ]
)

# and urlpatterns to include
urlpatterns = Site().build().urlpatterns
