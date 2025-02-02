from django.apps import AppConfig


class SongmanagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'SongManager'

    def ready(self):
        import SongManager.signals
