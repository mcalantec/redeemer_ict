# create_admin.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ict_ticketing.settings')  # Use your actual settings path
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "P@55w0rd@1")

try:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print("✅ Superuser created.")
    else:
        print("ℹ️ Superuser already exists.")
except Exception as e:
    print("❌ Error creating superuser:", str(e))

