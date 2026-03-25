from django.apps import AppConfig
import sys

class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self):
        import dashboard.routing
        
        if 'runserver' in sys.argv:
            import dashboard.mqtt_client
