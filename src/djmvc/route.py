from django.urls import reverse


class Route:
    @property
    def title(self):
        return type(self).__name__

    @property
    def codename(self):
        return type(self).__name__.replace(' ', '_').lower()

    def __str__(self):
        return self.title

    @property
    def urlpath(self):
        return self.codename + '/'

    @property
    def urlname(self):
        return self.codename

    @property
    def urlpatterns(self):
        raise NotImplementedError('Use Controller or View classes')

    @property
    def urlfullname(self):
        name = self.urlname
        current = self
        while parent := getattr(current, 'controller', None):
            name = f'{parent.urlname}:{name}'
            current = parent
        return name

    @property
    def url(self):
        return self.reverse()

    def reverse(self, *args, **kwargs):
        return reverse(self.urlfullname, args=args, kwargs=kwargs)
