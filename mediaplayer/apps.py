from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class DjangocmsMediaplayerConfig(AppConfig):
    name = 'mediaplayer'
    verbose_name = _('DjangoCMS Media Player')

    def __init__(self, app_name, app_module):
        if 'cmsplus' not in settings.INSTALLED_APPS:
            settings.INSTALLED_APPS += ["cmsplus", ]
        super().__init__(app_name, app_module)
