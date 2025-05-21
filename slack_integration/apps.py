from django.apps import AppConfig

class SlackIntegrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'slack_integration'

    def ready(self):
        print("SlackIntegrationConfig.ready() called")
        import slack_integration.signals
        print("Slack signals imported successfully")