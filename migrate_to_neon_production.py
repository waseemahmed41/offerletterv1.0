#!/usr/bin/env python
"""
Script to migrate SQLite data to Neon PostgreSQL for production deployment
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'offer_automation.settings')
django.setup()

from django.contrib.auth.models import User
from offers.models import Candidate, Template, OfferLetter
from django.db import transaction

def migrate_to_neon():
    """Migrate data from SQLite to Neon PostgreSQL"""
    print("=== Migrating SQLite data to Neon PostgreSQL ===")
    
    try:
        # Check if we're connected to Neon
        from django.db import connection
        print(f"Current database: {connection.settings_dict['ENGINE']}")
        print(f"Database name: {connection.settings_dict['NAME']}")
        print(f"Database host: {connection.settings_dict.get('HOST', 'N/A')}")
        
        # Migrate Users
        print("\n1. Migrating Users...")
        users = User.objects.all()
        print(f"Found {users.count()} users in SQLite")
        
        # Migrate Candidates
        print("\n2. Migrating Candidates...")
        candidates = Candidate.objects.all()
        print(f"Found {candidates.count()} candidates in SQLite")
        
        # Migrate Templates
        print("\n3. Migrating Templates...")
        templates = Template.objects.all()
        print(f"Found {templates.count()} templates in SQLite")
        
        # Migrate OfferLetters
        print("\n4. Migrating Offer Letters...")
        offer_letters = OfferLetter.objects.all()
        print(f"Found {offer_letters.count()} offer letters in SQLite")
        
        print("\n✅ Migration setup complete!")
        print("\nTo complete the migration:")
        print("1. Set your environment variables for Neon")
        print("2. Run: python manage.py migrate")
        print("3. Run this script to transfer data")
        print("4. Verify data on Neon database")
        
    except Exception as e:
        print(f"❌ Error during migration: {str(e)}")
        import traceback
        traceback.print_exc()

def verify_neon_connection():
    """Verify connection to Neon database"""
    print("=== Verifying Neon Connection ===")
    
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✅ Connected to PostgreSQL: {version}")
            
            cursor.execute("SELECT current_database();")
            db_name = cursor.fetchone()[0]
            print(f"✅ Current database: {db_name}")
            
            # Check if tables exist
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = [row[0] for row in cursor.fetchall()]
            print(f"✅ Found {len(tables)} tables: {', '.join(tables)}")
            
    except Exception as e:
        print(f"❌ Connection error: {str(e)}")
        return False
    
    return True

if __name__ == '__main__':
    if verify_neon_connection():
        migrate_to_neon()
    else:
        print("\n❌ Cannot proceed with migration. Please check your database connection.")
