from djmvc.view import ViewMixin
from django.views import generic


class TemplateMixin:
    """Expose ``view`` in template context and resolve template names.

    Concrete views set :attr:`default_template_name` or :attr:`template_name`.
    Resolution order is documented in :meth:`get_template_names`.
    """

    def get_context_data(self, *args, **kwargs):
        """Add ``view`` to the template context."""
        context = super().get_context_data(*args, **kwargs)
        context['view'] = self
        return context

    def get_template_names(self):
        """Resolve templates from most specific (controller/view) to generic."""
        template_names = []

        # whatever was set goes first
        if template_name := getattr(self, 'template_name', None):
            template_names.append(template_name)

        # build various combinations, from most specifc to least specific
        current = self
        template_name = f'{self.codename.lower()}.html'
        template_names.append(template_name)
        while parent := getattr(current, 'controller', None):
            if not parent.codename:
                continue
            template_name = f'{parent.codename.lower()}/{template_name}'
            template_names.insert(0, template_name)
            current = parent

        # give a chance to a default_template_name
        if default := getattr(self, 'default_template_name', None):
            template_names.append(default)

        # also prefix all template names with djmvc/ for users with
        # legacy/mixed projects who need a namespace
        template_names = [
            f'djmvc/{name}' for name in template_names
        ] + template_names

        return template_names


class TemplateViewMixin(ViewMixin, TemplateMixin):
    pass


class TemplateView(TemplateViewMixin, generic.TemplateView):
    """Static template page with djmvc layout and ``view`` in context."""
    pass
