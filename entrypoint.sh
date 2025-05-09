#!/usr/bin/env sh
set -e

# 1. Run migrations
echo "Running migrations…"
python3 manage.py makemigrations --noinput
python3 manage.py migrate --fake-initial --noinput

# preapre static files
echo "Collecting static files…"
python3 manage.py collectstatic --noinput

# Check if DJANGO_DB_LOCATION is set and if the file exists
if [ -n "$DJANGO_DB_LOCATION" ]; then
    echo "DJANGO_DB_LOCATION is set to: $DJANGO_DB_LOCATION"
    if [ -f "$DJANGO_DB_LOCATION" ]; then
        echo "Database file exists at $DJANGO_DB_LOCATION"
    else
        echo "WARNING: Database file does not exist at $DJANGO_DB_LOCATION"
        exit 2
    fi
else
    echo "DJANGO_DB_LOCATION is not set"
    exit 1
fi

# 2. Create superuser if not exists
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ]; then
  echo "Checking for existing superuser…"
  python3 manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
username = "$DJANGO_SUPERUSER_USERNAME"
email = "$DJANGO_SUPERUSER_EMAIL"
password = "$DJANGO_SUPERUSER_PASSWORD"
if not User.objects.filter(username=username).exists():
    print("Creating superuser '$DJANGO_SUPERUSER_USERNAME'")
    User.objects.create_superuser(username, email, password)
else:
    print("Superuser '$DJANGO_SUPERUSER_USERNAME' already exists")
EOF
else
  echo "WARNING: DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, and DJANGO_SUPERUSER_PASSWORD must be set to auto-create a superuser"
fi

# 3. Execute main container command
exec "$@"
