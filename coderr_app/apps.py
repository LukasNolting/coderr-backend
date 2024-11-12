from django.apps import AppConfig


class CoderrAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coderr_app'
    def ready(self):
        import auth_app.signals