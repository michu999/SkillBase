from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from bot.models import User
from slack_integration.services import SlackProfileService

@receiver(m2m_changed, sender=User.skills.through)
def update_slack_profile(sender, instance, action, **kwargs):
    """Update Slack profile when skills are changed."""
    if action in ["post_add", "post_remove", "post_clear"]:
        slack_service = SlackProfileService()
        slack_service.update_user_profile(
            user_id=instance.user_id,  # Slack user ID
            skills=[skill.name for skill in instance.skills.all()],  # List of skill names
            city=instance.city.name if instance.city else ""  # City name
        )