#!/usr/bin/env python
"""
Check Neon database status
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
from django.db import connection

def check_neon():
    """Check Neon database status"""
    print("=== Neon Database Status ===")
    print(f"Database: {connection.settings_dict['NAME']}")
    print(f"Engine: {connection.settings_dict['ENGINE']}")
    
    candidate_count = Candidate.objects.count()
    offer_letter_count = OfferLetter.objects.count()
    
    print(f"Candidates: {candidate_count}")
    print(f"Offer Letters: {offer_letter_count}")
    
    if candidate_count > 0:
        print("\nCandidates in Neon:")
        for candidate in Candidate.objects.all().order_by('work_id'):
            print(f"  {candidate.work_id}: {candidate.name}")

if __name__ == '__main__':
    check_neon()
