from django.views import generic

from .template import TemplateViewMixin


class ObjectMixin:
    @property
    def urlpath(self):
        return f'<pk>/{self.codename}/'

    @property
    def title(self):
        return f'{self.object} {self.model._meta.verbose_name.capitalize()} {super().title}'

    def breadcrumbs(self, with_self=True):
        crumbs = []
        list_route = self.controller.find_route('list')
        if list_route:
            list_view = type(list_route)(request=self.request)
            if list_view.has_permission():
                crumbs.append(list_view)

        detail_route = self.controller.find_route('detail')
        if detail_route:
            detail_view = type(detail_route)(request=self.request, object=self.object)
            if detail_view.has_permission():
                crumbs.append(detail_view)

        if with_self:
            crumbs.append(self)
        return crumbs


class ObjectTemplateView(ObjectMixin, TemplateViewMixin, generic.TemplateView):
    tags = ['object']