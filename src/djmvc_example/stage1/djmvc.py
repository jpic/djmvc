import djmvc

from .models import Document


class Stage1Controller(djmvc.ModelController):
    """Scoped querysets and view-level permissions."""

    model = Document

    @property
    def codename(self):
        return "stage1"

    routes = [
        djmvc.generic.ListView.clone(permission_shortcode="view"),
        djmvc.generic.DetailView.clone(permission_shortcode="view"),
        djmvc.generic.UpdateView,
        djmvc.generic.DeleteView,
        djmvc.generic.DeleteObjectsView,
        djmvc.generic.CreateView,
    ]

    def get_queryset(self, view):
        qs = super().get_queryset(view)
        user = view.request.user
        if user.is_superuser:
            return qs
        return qs.filter(owner=user)

    def has_permission(self, view):
        if view.permission_shortcode == "view":
            return view.has_permission_backend()
        return super().has_permission(view)


djmvc.site.routes.append(Stage1Controller)