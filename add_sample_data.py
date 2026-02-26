#!/usr/bin/env python
import os
import sys
import django
from datetime import date, timedelta

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'offer_automation.settings')
django.setup()

from offers.models import Candidate, Template, OfferLetter
from accounts.models import User

def add_sample_data():
    """Add sample candidates and offer letters"""
    print("Adding sample data...")
    
    # Get admin user
    try:
        admin_user = User.objects.get(username='admin')
    except User.DoesNotExist:
        print("Admin user not found!")
        return
    
    # Sample candidates data
    sample_candidates = [
        {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '+1234567890',
            'role': 'frontend',
            'letter_date': date.today(),
            'joining_date': date.today() + timedelta(days=30),
            'status': 'pending'
        },
        {
            'name': 'Jane Smith',
            'email': 'jane.smith@example.com',
            'phone': '+0987654321',
            'role': 'backend',
            'letter_date': date.today(),
            'joining_date': date.today() + timedelta(days=45),
            'status': 'offer_generated'
        },
        {
            'name': 'Mike Johnson',
            'email': 'mike.johnson@example.com',
            'phone': '+1122334455',
            'role': 'full_stack',
            'letter_date': date.today(),
            'joining_date': date.today() + timedelta(days=60),
            'status': 'offer_sent'
        }
    ]
    
    # Add candidates
    for candidate_data in sample_candidates:
        candidate = Candidate(
            name=candidate_data['name'],
            email=candidate_data['email'],
            phone=candidate_data['phone'],
            role=candidate_data['role'],
            letter_date=candidate_data['letter_date'],
            joining_date=candidate_data['joining_date'],
            status=candidate_data['status'],
            created_by_id=admin_user.id,
            created_by_username=admin_user.username
        )
        candidate.save()
        print(f"Added candidate: {candidate.name} ({candidate.work_id})")
    
    print(f"\nTotal candidates: {Candidate.objects.count()}")
    print("Sample data added successfully!")

if __name__ == '__main__':
    add_sample_data()
