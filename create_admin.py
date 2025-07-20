# create_admin.py
import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ict_ticketing.settings')
django.setup()

User = get_user_model()

username = 'admin'
password = 'P@55w0rd@1'
email = 'admin@example.com'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, password=password, email=email)
    print("✅ Superuser created.")
else:
    print("⚠️ Superuser already exists.")
