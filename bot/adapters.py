from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        # Use Slack data for username if available
        if sociallogin.account.provider == 'slack':
            slack_data = sociallogin.account.extra_data
            user_info = slack_data.get('user', {})

            # Try different fields for username
            username = (user_info.get('name') or
                        user_info.get('real_name') or
                        user_info.get('email') or
                        user_info.get('id'))

            if username:
                user.username = username

        return user

    def is_auto_signup_allowed(self, request, sociallogin):
        # Always allow auto-signup
        return True