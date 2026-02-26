#!/usr/bin/env python
"""
Remove specific users from Neon database, keeping only specified ones
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
from django.db import transaction

def remove_specific_users():
    """Remove users except the specified ones"""
    print("=== Removing Specific Users from Neon Database ===")
    
    # Users to keep
    users_to_keep = [
        'waseem@thome',
        'pratheek@thome', 
        'ravinder@thome',
        'revanth@thome'
    ]
    
    print(f"Users to keep: {users_to_keep}")
    
    # Get all users
    all_users = User.objects.all()
    print(f"\nTotal users in database: {all_users.count()}")
    
    print("\nCurrent users:")
    for user in all_users:
        status = "KEEP" if user.username in users_to_keep else "REMOVE"
        print(f"  [{status}] {user.username} ({user.email})")
    
    # Find users to remove
    users_to_remove = all_users.exclude(username__in=users_to_keep)
    
    if users_to_remove.count() == 0:
        print("\n✅ No users to remove. All specified users are already the only ones present.")
        return
    
    print(f"\nUsers to be removed ({users_to_remove.count()}):")
    for user in users_to_remove:
        print(f"  - {user.username} ({user.email})")
    
    # Confirm deletion
    response = input("\nAre you sure you want to remove these users? (yes/no): ")
    if response.lower() != 'yes':
        print("Operation cancelled.")
        return
    
    # Delete users in transaction
    with transaction.atomic():
        deleted_count = 0
        for user in users_to_remove:
            print(f"Deleting: {user.username}")
            user.delete()
            deleted_count += 1
        
        print(f"\n✅ Successfully deleted {deleted_count} users!")
    
    # Show final state
    print("\n=== Final User List ===")
    remaining_users = User.objects.all()
    print(f"Total users remaining: {remaining_users.count()}")
    
    for user in remaining_users:
        print(f"  - {user.username} ({user.email})")
        print(f"    Staff: {user.is_staff}, Superuser: {user.is_superuser}, Active: {user.is_active}")

if __name__ == '__main__':
    remove_specific_users()
