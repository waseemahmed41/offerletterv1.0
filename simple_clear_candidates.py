#!/usr/bin/env python
"""
Simple script to clear candidates from current database
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
from django.db import transaction

def clear_current_database():
    """Clear candidates from current database"""
    print("=== Clearing Candidates from Current Database ===")
    
    try:
        # Check which database we're connected to
        from django.db import connection
        db_name = connection.settings_dict['NAME']
        db_engine = connection.settings_dict['ENGINE']
        print(f"Connected to: {db_engine}")
        print(f"Database name: {db_name}")
        
        # Count before deletion
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
        
        # Delete in transaction
        with transaction.atomic():
            # First delete offer letters
            deleted_offer_letters = OfferLetter.objects.all().delete()[0]
            print(f"\nDeleted {deleted_offer_letters} offer letters")
            
            # Then delete candidates
            deleted_candidates = Candidate.objects.all().delete()[0]
            print(f"Deleted {deleted_candidates} candidates")
        
        print("\n✅ Successfully cleared all candidates and offer letters!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("This will clear all candidates from the current database.")
    print("Current database is based on your environment variables.")
    print("\nTo clear SQLite: Run without DB_HOST set")
    print("To clear Neon: Set DB_HOST and other Neon env vars")
    print()
    
    clear_current_database()
