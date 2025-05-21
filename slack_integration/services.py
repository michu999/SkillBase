import logging
import requests
import json
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

        data = {
            "user": user_id,
            "profile": {
                "fields": {
                    "Xf08NAUR6K1N": {  # Skills field ID
                        "value": ", ".join(skills) if skills else "",
                        "alt": ""
                    },
                    "Xf08PMME6KJS": {  # City field ID
                        "value": city if city else "",
                        "alt": ""
                    }
                }
            }
        }

        url = "https://slack.com/api/users.profile.set"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json; charset=utf-8"
        }

        # Add retry logic for rate limits
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(url, headers=headers, json=data)
                response_data = response.json()

                if response.status_code == 200 and response_data.get("ok"):
                    return True
                elif response.status_code == 429:  # Rate limited
                    retry_after = int(response.headers.get('Retry-After', 5))
                    logger.warning(f"Rate limited. Waiting {retry_after}s. Attempt {attempt + 1}/{max_retries}")
                    time.sleep(retry_after)  # Wait before retrying
                    continue
                else:
                    logger.error(f"Slack API error: {response.status_code}, {response_data}")
                    return False

            except Exception as e:
                logger.exception(f"Error updating Slack profile: {e}")
                return False

        logger.error(f"Failed after {max_retries} attempts due to rate limiting")
        return False