#!/usr/bin/env python
"""
Check users in Neon database
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'offer_automation.settings')
django.setup()

from accounts.models import User
from django.db import connection

def check_neon_users():
    """Check users in Neon database"""
    print("=== Neon Database Users ===")
    print(f"Database: {connection.settings_dict['NAME']}")
    print(f"Engine: {connection.settings_dict['ENGINE']}")
    
    user_count = User.objects.count()
    print(f"\nTotal Users: {user_count}")
    
    if user_count > 0:
        print("\nUser Details:")
        for user in User.objects.all():
            print(f"  - {user.username} ({user.email})")
            print(f"    Staff: {user.is_staff}, Superuser: {user.is_superuser}, Active: {user.is_active}")
            print(f"    Date Joined: {user.date_joined}")
            print()
    else:
        print("No users found in Neon database.")

if __name__ == '__main__':
    check_neon_users()
