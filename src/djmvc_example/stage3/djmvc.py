from django import forms

import djmvc

from .models import Post


class SetCategoryForm(forms.Form):
    category = forms.CharField(max_length=50, label="Category")


class SetCategoryView(djmvc.generic.ListActionView):
    """Bulk-update category on selected rows."""

    title = "Set category"
    icon = "tag"
    color = "info"
    message = "Choose a category for the selected posts."
    form_class = SetCategoryForm

    def form_valid(self, form):
        self.object_list.update(category=form.cleaned_data["category"])
        return super().form_valid(form)

    def get_form_valid_message(self):
        count = self.object_list.count()
        return f"Updated category on {count} post(s)."


class Stage3Controller(djmvc.ModelController):
    model = Post

    @property
    def codename(self):
        return "stage3"

    routes = [
        djmvc.generic.ListView,
        djmvc.generic.DetailView,
        djmvc.generic.UpdateView,
        djmvc.generic.DeleteView,
        djmvc.generic.CreateView,
        SetCategoryView,
        djmvc.generic.DeleteObjectsView,
    ]


djmvc.site.routes.append(Stage3Controller)