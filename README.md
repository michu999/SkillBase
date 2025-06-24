# SkillBase

SkillBase is a Django-based application that integrates with Slack to manage user skills, location, and section. Users can log in via Slack, add their skills, city, and section, and the application automatically updates this information in their Slack profile. A Slack command is also available to search for users with specific skills.

## Features

-   **Slack OAuth Integration**: Users sign in with their Slack account.
-   **Skill Management**: Users can add and update their skills.
-   **Location and Section Tracking**: Tracks user's city and organizational section.
-   **Slack Profile Synchronization**: Automatically updates custom fields in Slack profiles.
-   **Slack Commands**: Use `/findskill [skill]` to find users with specific skills.
-   **REST API**: Access user data programmatically.

## Setup Instructions

### Prerequisites

-   Python 3.8+
-   Django 5.2+
-   Slack Workspace with admin privileges
-   Docker (optional)

### Local Development Setup

1.  Clone the repository:

    ```bash
    git clone https://github.com/michu999/SkillBase.git
    cd SkillBase
    ```

2.  Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4.  Configure environment variables in `.env` file:

    ```
    DJANGO_SECRET_KEY=your_secret_key
    DEBUG=True
    DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
    SLACK_BOT_TOKEN=your_slack_bot_token
    ```

5.  Create SSL certificates for development:

    ```bash
    mkdir -p certs
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout certs/key.pem -out certs/cert.pem
    ```

6.  Run migrations:

    ```bash
    python manage.py migrate
    ```

7.  Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

8.  Run the development server:

    ```bash
    python manage.py runserver_plus --cert-file certs/cert.pem --key-file certs/key.pem 0.0.0.0:8443
    ```

### Docker Setup

```bash
docker-compose up
```
### Slack Configuration

#### Slack App Setup

1.  Create a new Slack App at [api.slack.com/apps](https://api.slack.com/apps)
2.  Enable OAuth and set the following scopes:
    -   `openid`
    -   `email`
    -   `profile`
3.  Add OAuth Redirect URLs pointing to your app's `/accounts/slack/login/callback/` endpoint
4.  Install the app to your workspace

#### Important: Custom Profile Fields Configuration

⚠️ **You must update the field IDs in `slack_integration/services.py` to match your Slack workspace's custom profile fields.**

In the `update_user_profile` method of `SlackProfileService`, you need to change the field IDs to match your Slack workspace's custom profile fields.

Example:

```python
"Xf08NAUR6K1N": {  # Skills field ID
    "value": ", ".join(skills) if skills else "",
    "alt": ""
},
"Xf03VBLQB0TA": {  # City field ID
    "value": city if city else "",
    "alt": ""
},
"Xf08PMME6KJS": {  # Section field ID
    "value": section if section else "",
    "alt": ""
}
```
1. Create custom profile fields in your Slack workspace:  
   _Admin → Settings & Permissions → Profiles_

2. Use the Slack API explorer or your browser's developer tools to inspect your profile and locate the field IDs for your custom fields.

## API Documentation

The REST API provides the following endpoints:

- `GET /api/users/` - List all users
- `GET /api/users/{id}/` - Get specific user details
- `GET /api/skills/` - List all skills in the system

For more details, see the API documentation in the `/docs` endpoint when running the application.

## Testing

Run the test suite with:

```bash
python manage.py test
```
