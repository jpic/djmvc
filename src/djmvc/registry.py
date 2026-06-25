class Registry:
    def __init__(self, controller, routes=()):
        self.controller = controller
        self._items = []
        self._by_codename = {}
        for route in routes:
            self.register(route)

    def register(self, route):
        cls = route if isinstance(route, type) else type(route)
        cls = cls.clone(controller=self.controller)
        instance = cls()
        self._by_codename[instance.codename] = instance
        self._items.append(instance)
        return instance

    def __setitem__(self, codename, route):
        cls = route if isinstance(route, type) else type(route)
        cls = cls.clone(controller=self.controller)
        instance = cls()
        if codename in self._by_codename:
            old = self._by_codename[codename]
            self._items[self._items.index(old)] = instance
        else:
            self._items.append(instance)
        self._by_codename[codename] = instance

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._items[key]
        return self._by_codename[key]

    def __delitem__(self, codename):
        instance = self._by_codename.pop(codename)
        self._items.remove(instance)

    def __iter__(self):
        return iter(self._items)