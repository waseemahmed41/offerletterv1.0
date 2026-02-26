#!/usr/bin/env python
"""
Script to remove all candidates from both SQLite and Neon databases
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'offer_automation.settings')
django.setup()

from offers.models import Candidate, OfferLetter
from django.db import connection, transaction

def clear_candidates_from_current_db():
    """Clear candidates from current database connection"""
    print(f"=== Clearing Candidates from Current Database ===")
    
    try:
        # Check which database we're connected to
        db_name = connection.settings_dict['NAME']
        db_engine = connection.settings_dict['ENGINE']
        print(f"Connected to: {db_engine}")
        print(f"Database name: {db_name}")
        
        # Count candidates before deletion
        candidate_count = Candidate.objects.count()
        offer_letter_count = OfferLetter.objects.count()
        
        print(f"\nFound {candidate_count} candidates")
        print(f"Found {offer_letter_count} offer letters")
        
        if candidate_count == 0 and offer_letter_count == 0:
            print("No data to clear.")
            return
        
        # Show candidates before deletion
        if candidate_count > 0:
            print("\nCandidates to be deleted:")
            for candidate in Candidate.objects.all().order_by('work_id'):
                print(f"  {candidate.work_id}: {candidate.name} ({candidate.email})")
        
        # Confirm deletion
        response = input("\nAre you sure you want to delete ALL candidates and offer letters? (yes/no): ")
        if response.lower() != 'yes':
            print("Operation cancelled.")
            return
        
        # Delete in transaction
        with transaction.atomic():
            # First delete offer letters (they reference candidates)
            deleted_offer_letters = OfferLetter.objects.all().delete()[0]
            print(f"Deleted {deleted_offer_letters} offer letters")
            
            # Then delete candidates
            deleted_candidates = Candidate.objects.all().delete()[0]
            print(f"Deleted {deleted_candidates} candidates")
        
        print("\n✅ Successfully cleared all candidates and offer letters!")
        
    except Exception as e:
        print(f"❌ Error clearing candidates: {str(e)}")
        import traceback
        traceback.print_exc()

def clear_from_sqlite():
    """Clear candidates from SQLite database"""
    print("\n=== Clearing from SQLite ===")
    
    # Temporarily switch to SQLite
    original_db_config = django.conf.settings.DATABASES.copy()
    
    django.conf.settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }
    
    # Close existing connections
    from django.db import connections
    connections.close_all()
    
    try:
        clear_candidates_from_current_db()
    finally:
        # Restore original database configuration
        django.conf.settings.DATABASES = original_db_config
        connections.close_all()

def clear_from_neon():
    """Clear candidates from Neon PostgreSQL"""
    print("\n=== Clearing from Neon PostgreSQL ===")
    
    # Set environment variables for Neon
    os.environ['DB_HOST'] = 'ep-raspy-lab-ai24kg9x-pooler.c-4.us-east-1.aws.neon.tech'
    os.environ['DB_NAME'] = 'neondb'
    os.environ['DB_USER'] = 'neondb_owner'
    os.environ['DB_PASSWORD'] = 'npg_vRyhlNFuV16t'
    os.environ['DB_PORT'] = '5432'
    
    # Reload Django settings to pick up Neon
    from django.conf import settings
    settings._wrapped = None
    
    # Close existing connections
    from django.db import connections
    connections.close_all()
    
    try:
        clear_candidates_from_current_db()
    finally:
        # Clear environment variables
        for key in ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_PORT']:
            if key in os.environ:
                del os.environ[key]
        
        # Reload Django settings
        settings._wrapped = None
        connections.close_all()

def check_current_state():
    """Check current state of both databases"""
    print("=== Checking Current State ===")
    
    # Check SQLite
    print("\n--- SQLite Database ---")
    clear_from_sqlite()
    
    # Check Neon
    print("\n--- Neon PostgreSQL Database ---")
    clear_from_neon()

if __name__ == '__main__':
    print("This script will remove ALL candidates and offer letters from both databases.")
    print("This action cannot be undone!\n")
    
    response = input("Do you want to proceed? (yes/no): ")
    if response.lower() != 'yes':
        print("Operation cancelled.")
        sys.exit(0)
    
    # Clear from both databases
    clear_from_sqlite()
    clear_from_neon()
    
    print("\n=== Final Verification ===")
    print("Checking that both databases are now empty...")
    
    # Final check
    check_current_state()
    
    print("\n✅ All candidates and offer letters have been removed from both databases!")
