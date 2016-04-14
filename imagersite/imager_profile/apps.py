from django.apps import AppConfig


class ImagerProfileConfig(AppConfig):
    name = 'imager_profile'

    def ready(self):
        from imager_profile import handlers
