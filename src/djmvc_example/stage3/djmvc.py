import djmvc

from .models import Article


class CategoryUpdateView(djmvc.generic.UpdateView):
    """Update a single field — shows in the object action menu."""

    fields = ["category"]
    title = "Change category"
    icon = "tag"
    color = "info"


class ArticleController(djmvc.ModelController):
    model = Article
    icon = 'newspaper'

    routes = djmvc.ModelController.routes + [
        djmvc.generic.ListView.clone(
            table_fields=["title", "category"],
            filter_fields=["category"],
            paginate_by=5,
        ),
        CategoryUpdateView,
    ]


djmvc.site.routes.append(ArticleController)