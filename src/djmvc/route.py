

class Route:
    @property
    def name(self):
        return type(self).__name__

    @property
    def urlpath(self):
        return self.name.lower() + '/'

    @property
    def urlname(self):
        return self.name.lower()

    @property
    def urlpatterns(self):
        raise NotImplementedError('Use Controller or View classes')
