from django.apps import AppConfig


class ImagerImagesConfig(AppConfig):
    name = 'imager_images'

    def ready(self):
        from imager_images import handlers
