from dal_alight.views import AlightQuerySetView

from djmvc.model import ModelMixin
from djmvc.view import ViewMixin


class AutocompleteView(ModelMixin, ViewMixin, AlightQuerySetView):
    """DAL Alight autocomplete endpoint for a model controller's rows."""

    permission_shortcode = 'view'
    tags = []

    def get_search_fields(self):
        list_route = self.controller.find_route('list')
        if list_route is not None:
            return type(list_route)().search_fields
        return super().get_search_fields()