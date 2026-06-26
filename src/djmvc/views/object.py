from django.views import generic

from .template import TemplateViewMixin


class ObjectMixin:
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.object = self.get_object()

    def get_object(self):
        if obj := getattr(self, 'object', None):
            return obj
        pk = self.kwargs.get('pk')
        return self.model._default_manager.get(pk=pk)

    @property
    def url(self):
        # object bound on the view instance
        if obj := getattr(self, 'object', None):
            return self.reverse(obj.pk)
        # pk bound from URL kwargs during dispatch
        if pk := getattr(self, 'kwargs', {}).get('pk'):
            return self.reverse(pk)
        return super().url

    @property
    def urlpath(self):
        return f'<pk>/{self.codename}/'

    @property
    def breadcrumb_title(self):
        return self.title

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