from django.http import HttpResponseRedirect
from django.urls import reverse

# Disable Unpoly on links that must reload the full document (menus, session).
FULL_PAGE_LINK_ATTRIBUTES = {'up-follow': False}


def home_url(request):
    import djmvc

    if not hasattr(djmvc.site, 'registry'):
        djmvc.site.build()
    home_route = djmvc.site.find_route('home')
    if home_route is not None:
        return type(home_route)(request=request).url
    return reverse('site:home')


def full_page_redirect(url):
    """Redirect after an identity-changing action (browser follows natively)."""
    return HttpResponseRedirect(url)


def full_page_redirect_home(request):
    return full_page_redirect(home_url(request))