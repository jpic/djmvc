import djmvc

from .models import Article


class CategoryUpdateView(djmvc.generic.UpdateView):
    """Update a single field — shows in the object action menu."""

    fields = ["category"]
    title = "Change category"
    icon = "tag"
    color = "info"


class Stage2Controller(djmvc.ModelController):
    model = Article

    @property
    def codename(self):
        return "stage2"

    routes = [
        djmvc.generic.ListView.clone(
            table_fields=["title", "category"],
            filter_fields=["category"],
            paginate_by=5,
        ),
        djmvc.generic.DetailView,
        djmvc.generic.UpdateView,
        CategoryUpdateView,
        djmvc.generic.DeleteView,
        djmvc.generic.DeleteObjectsView,
        djmvc.generic.CreateView,
    ]


djmvc.site.routes.append(Stage2Controller)