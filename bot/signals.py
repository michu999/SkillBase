from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User as AuthUser
from allauth.socialaccount.models import SocialAccount
from allauth.account.signals import user_signed_up
from .models import User as BotUser  # Rename to avoid conflict


@receiver(user_signed_up)
def create_user_profile(sender, request, user, **kwargs):
    """Create a User profile when a new user signs up via Slack"""
    try:
        # Check if the user signed up with Slack
        social_account = SocialAccount.objects.filter(user=user, provider='slack').first()

        if social_account:
            extra_data = social_account.extra_data
            user_info = extra_data.get('user', {})

            # Get name details
            name = user_info.get('name', '') or user_info.get('real_name', '')
            name_parts = name.split(' ', 1)
            first_name = name_parts[0] if name_parts else user.username
            last_name = name_parts[1] if len(name_parts) > 1 else ''

            # Get email
            email = user_info.get('email') or user.email or ''

            # Create or update the custom User model
            BotUser.objects.update_or_create(
                auth_user=user,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email
                }
            )
    except Exception as e:
        print(f"Error creating user profile: {e}")