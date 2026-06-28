import djmvc

from .models import Document


class DocumentController(djmvc.ModelController):
    model = Document

    def get_queryset(self, view):
        qs = super().get_queryset(view)
        user = view.request.user
        if user.is_superuser:
            return qs
        return qs.filter(owner=user)


djmvc.site.routes.append(DocumentController)