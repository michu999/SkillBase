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

    # Debug the actual values to see what's in the database
    logger.info(
        f"User data: id={instance.id}, user_id={instance.user_id}, slack_id={getattr(instance, 'slack_id', 'N/A')}")

    # Check where the Slack ID is actually stored
    # Try other potential attribute names
    slack_user_id = instance.user_id or getattr(instance, 'slack_id', None) or getattr(instance, 'slack_user_id', None)

    if not slack_user_id:
        logger.warning(f"User {instance.id} has no Slack user_id - check data in admin panel")
        return False

    # Use the correct variable for the rest of the function
    skills = [skill.name for skill in instance.skills.all()]
    city = instance.city.name if instance.city else ""
    section = instance.section.name if instance.section else ""

    slack_service = SlackProfileService()
    result = slack_service.update_user_profile(
        user_id=slack_user_id,  # Use the correct variable
        skills=skills,
        city=city,
        section=section
    )

    return result


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
    # Check if this is a recursive call from within update_slack_profile
    if getattr(instance, '_updating_slack', False):
        return
    logger.info(f"SIGNAL: post_save detected for User {instance.id}, created={created}")
    update_slack_profile(instance)
