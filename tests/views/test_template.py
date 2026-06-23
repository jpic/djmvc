from djmvc.views.generic import TemplateView


def test_get_context_data():
    view = TemplateView()
    assert view.get_context_data()['view'] is view
