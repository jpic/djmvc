from djmvc.view import ViewMixin
from django.views import generic


class TemplateMixin:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['view'] = self
        return context


class TemplateView(ViewMixin, TemplateMixin, generic.TemplateView):
    pass
