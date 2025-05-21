import logging
import requests
import time
from django.conf import settings

logger = logging.getLogger(__name__)

class SlackProfileService:
    def __init__(self):
        self.base_url = "https://slack.com/api"
        self.token = settings.SLACK_BOT_TOKEN

    def update_user_profile(self, user_id, skills, city):
        """Update a user's Slack profile with their skills and city."""
        if not user_id:
            logger.error("Cannot update profile: No user_id provided")
            return False

        # Prepare the custom fields for Skills and City
        profile_data = {
            "fields": {
                "Skills": {  # Replace with the actual field ID for "Skills"
                    "value": ", ".join(skills),  # Join skills into a comma-separated string
                    "alt": "Skills"
                },
                "City": {  # Replace with the actual field ID for "City"
                    "value": city,
                    "alt": "City"
                }
            }
        }

        url = f"{self.base_url}/users.profile.set"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        data = {
            "user": user_id,
            "profile": profile_data
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()

            if response.status_code == 200 and response_data.get("ok"):
                logger.info(f"Updated profile for user {user_id}")
                return True

            elif response.status_code == 429: #Rate limit error
                retry_after = response_data.get("headers", {}).get("Retry-After")
                logger.warning(f"Rate limit exceeded. Retry after {retry_after} seconds.")
                time.sleep(retry_after)

        except Exception as e:
            logger.exception(f"Error updating Slack profile: {e}")
            return False