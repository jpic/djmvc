class ActionMixin:
    def has_permission(self):
        if super().has_permission():
            if getattr(self, 'object', None) is not None:
                return self.has_permission_object()
            return True
        return False

    def has_permission_object(self):
        return True