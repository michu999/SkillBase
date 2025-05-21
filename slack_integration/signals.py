import logging
import time
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from bot.models import User
from slack_integration.services import SlackProfileService

print("SIGNALS MODULE LOADED - slack_integration/signals.py")

logger = logging.getLogger(__name__)


# Helper function to update Slack profile
def update_slack_profile(instance):
    """Update Slack profile with user's skills and city."""
    logger.info(f"==== SIGNAL TRIGGERED: update_slack_profile for user_id: {instance.id} ====")
    print(f"==== SIGNAL TRIGGERED: update_slack_profile for user_id: {instance.id} ====")

    user_id = instance.user_id  # Slack user ID

    if not user_id:
        logger.warning(f"User {instance.id} has no Slack user_id")
        print(f"User {instance.id} has no Slack user_id")
        return

    skills = [skill.name for skill in instance.skills.all()]  # List of skill names
    city = instance.city.name if instance.city else ""  # City name

    logger.info(f"Updating Slack profile with data:")
    logger.info(f"User ID: {user_id}")
    logger.info(f"Skills: {skills}")
    logger.info(f"City: {city}")

    print(f"Updating Slack profile with data:")
    print(f"User ID: {user_id}")
    print(f"Skills: {skills}")
    print(f"City: {city}")

    slack_service = SlackProfileService()
    result = slack_service.update_user_profile(
        user_id=user_id,
        skills=skills,
        city=city
    )

    logger.info(f"Slack update result: {result}")
    print(f"Slack update result: {result}")


# Signal for ManyToMany changes (skills)
@receiver(m2m_changed, sender=User.skills.through)
def skills_changed(sender, instance, action, **kwargs):
    """Trigger when skills (ManyToMany) are changed."""
    logger.info(f"SIGNAL: m2m_changed detected for User.skills, action={action}")
    print(f"SIGNAL: m2m_changed detected for User.skills, action={action}")
    if action in ["post_add", "post_remove", "post_clear"]:
        update_slack_profile(instance)


# Signal for model saves (city and other fields)
@receiver(post_save, sender=User)
def user_saved(sender, instance, created, **kwargs):
    """Trigger when User model is saved (including city updates)."""
    logger.info(f"SIGNAL: post_save detected for User {instance.id}, created={created}")
    print(f"SIGNAL: post_save detected for User {instance.id}, created={created}")
    update_slack_profile(instance)