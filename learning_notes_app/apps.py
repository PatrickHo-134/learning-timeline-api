from django.apps import AppConfig


class LearningNotesAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "learning_notes_app"

    def ready(self):
        import learning_notes_app.signals