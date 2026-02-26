#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'offer_automation.settings')
django.setup()

from accounts.models import User

def set_admin_password():
    """Set password for admin user"""
    try:
        admin_user = User.objects.get(username='admin')
        admin_user.set_password('admin123')
        admin_user.save()
        print("Admin password set successfully!")
        print("Username: admin")
        print("Password: admin123")
    except User.DoesNotExist:
        print("Admin user not found!")

if __name__ == '__main__':
    set_admin_password()
