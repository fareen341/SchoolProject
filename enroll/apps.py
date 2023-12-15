from django.apps import AppConfig


class EnrollConfig(AppConfig):
    name = 'enroll'

    def ready(self):
        import enroll.signals

