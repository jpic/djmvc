from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class DjmvcDalConfig(AppConfig):
    name = 'djmvc_dal'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        for app in ('dal', 'dal_alight'):
            if app not in settings.INSTALLED_APPS:
                raise ImproperlyConfigured(
                    f'djmvc_dal requires {app!r} in INSTALLED_APPS'
                )
        try:
            import djhacker  # noqa: F401
        except ImportError as exc:
            raise ImproperlyConfigured(
                'djmvc_dal requires djhacker to be installed'
            ) from exc

        import djmvc_dal.models  # noqa: F401
        from . import hooks  # noqa: F401

        hooks.register()