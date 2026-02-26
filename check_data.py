#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'offer_automation.settings')
django.setup()

from offers.models import Candidate, Template, OfferLetter
from accounts.models import User

def check_sqlite_data():
    """Check what data exists in SQLite database"""
    print("=== SQLite Database Data ===")
    
    # Check Users
    users = User.objects.all()
    print(f"\nUsers: {users.count()}")
    for user in users:
        print(f"  - {user.username} ({user.email})")
    
    # Check Candidates
    candidates = Candidate.objects.all()
    print(f"\nCandidates: {candidates.count()}")
    for candidate in candidates:
        print(f"  - {candidate.work_id}: {candidate.name} ({candidate.email}) - {candidate.status}")
    
    # Check Templates
    templates = Template.objects.all()
    print(f"\nTemplates: {templates.count()}")
    for template in templates:
        role_display = f" ({template.get_role_display()})" if template.role else ""
        print(f"  - {template.name}{role_display} - Active: {template.is_active}")
    
    # Check Offer Letters
    offer_letters = OfferLetter.objects.all()
    print(f"\nOffer Letters: {offer_letters.count()}")
    for offer_letter in offer_letters:
        print(f"  - {offer_letter.candidate_work_id}: {offer_letter.template_name} - Sent: {offer_letter.sent_at}")

def check_neon_data():
    """Check what data exists in Neon database"""
    from django.db import connections
    
    print("\n=== Neon Database Data ===")
    
    # Check Candidates
    candidates = Candidate.objects.using('neon').all()
    print(f"\nCandidates: {candidates.count()}")
    for candidate in candidates:
        print(f"  - {candidate.work_id}: {candidate.name} ({candidate.email}) - {candidate.status}")
    
    # Check Templates
    templates = Template.objects.using('neon').all()
    print(f"\nTemplates: {templates.count()}")
    for template in templates:
        role_display = f" ({template.get_role_display()})" if template.role else ""
        print(f"  - {template.name}{role_display} - Active: {template.is_active}")
    
    # Check Offer Letters
    offer_letters = OfferLetter.objects.using('neon').all()
    print(f"\nOffer Letters: {offer_letters.count()}")
    for offer_letter in offer_letters:
        print(f"  - {offer_letter.candidate_work_id}: {offer_letter.template_name} - Sent: {offer_letter.sent_at}")

if __name__ == '__main__':
    check_sqlite_data()
    check_neon_data()
