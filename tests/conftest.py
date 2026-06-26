import pytest

import djmvc


@pytest.fixture(autouse=True)
def _autodiscover_routes():
    """Register per-app routes before tests (same as urls.py, without loading urlconf)."""
    djmvc.site.autodiscover()