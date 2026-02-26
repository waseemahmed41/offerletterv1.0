#!/usr/bin/env python
"""
Script to reset work_id sequence to start from 20 (0A20)
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'offer_automation.settings')
django.setup()

from offers.models import Candidate
from django.db import transaction

def reset_work_id_to_20():
    """Reset all work_ids to start from 20"""
    print("=== Resetting Work ID Sequence to Start from 20 ===")
    
    try:
        # Get all candidates ordered by current work_id
        candidates = Candidate.objects.all().order_by('work_id')
        print(f"Found {candidates.count()} candidates")
        
        if candidates.count() == 0:
            print("No candidates found. Nothing to reset.")
            return
        
        print("\nCurrent work_ids:")
        for candidate in candidates:
            print(f"  {candidate.work_id}: {candidate.name}")
        
        # Generate new work_ids starting from 0A20
        new_work_ids = []
        prefix = "0A"
        start_number = 20
        
        for i in range(candidates.count()):
            number = start_number + i
            if number > 99:
                # Handle progression to next prefix if needed
                prefix_letter = chr(ord('A') + (number - 100) // 100)
                number_in_prefix = ((number - 100) % 100) + 1
                new_work_id = f"0{prefix_letter}{number_in_prefix:02d}"
            else:
                new_work_id = f"{prefix}{number:02d}"
            new_work_ids.append(new_work_id)
        
        print(f"\nNew work_ids to assign:")
        for work_id in new_work_ids:
            print(f"  {work_id}")
        
        # Update work_ids in a transaction
        with transaction.atomic():
            for i, candidate in enumerate(candidates):
                old_work_id = candidate.work_id
                new_work_id = new_work_ids[i]
                candidate.work_id = new_work_id
                candidate.save()
                print(f"  Updated: {old_work_id} → {new_work_id} ({candidate.name})")
        
        print(f"\n✅ Successfully reset work_id sequence for {candidates.count()} candidates!")
        
        # Verify the update
        print("\nUpdated work_ids:")
        updated_candidates = Candidate.objects.all().order_by('work_id')
        for candidate in updated_candidates:
            print(f"  {candidate.work_id}: {candidate.name}")
            
    except Exception as e:
        print(f"❌ Error resetting work_ids: {str(e)}")
        import traceback
        traceback.print_exc()

def check_next_work_id():
    """Check what the next work_id will be"""
    print("\n=== Checking Next Work ID ===")
    
    try:
        next_work_id = Candidate.generate_work_id()
        print(f"Next work_id will be: {next_work_id}")
        
        # Show the last candidate
        last_candidate = Candidate.objects.order_by('-work_id').first()
        if last_candidate:
            print(f"Last candidate: {last_candidate.work_id} - {last_candidate.name}")
        else:
            print("No candidates found")
            
    except Exception as e:
        print(f"❌ Error checking next work_id: {str(e)}")

if __name__ == '__main__':
    reset_work_id_to_20()
    check_next_work_id()
