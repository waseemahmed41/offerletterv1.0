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

def migrate_data():
    """Migrate data from Neon PostgreSQL to SQLite"""
    print("Starting migration from Neon to SQLite...")
    
    # Migrate Candidates
    print("Migrating Candidates...")
    neon_candidates = Candidate.objects.using('neon').all()
    candidates_count = neon_candidates.count()
    print(f"Found {candidates_count} candidates in Neon database")
    
    for candidate in neon_candidates:
        # Check if candidate already exists in SQLite
        if not Candidate.objects.using('default').filter(work_id=candidate.work_id).exists():
            # Create new candidate in SQLite
            sqlite_candidate = Candidate(
                work_id=candidate.work_id,
                name=candidate.name,
                email=candidate.email,
                phone=candidate.phone,
                role=candidate.role,
                letter_date=candidate.letter_date,
                joining_date=candidate.joining_date,
                status=candidate.status,
                created_by_id=candidate.created_by_id,
                created_by_username=candidate.created_by_username,
                created_at=candidate.created_at,
                updated_at=candidate.updated_at
            )
            sqlite_candidate.save(using='default')
            print(f"Migrated candidate: {candidate.name} ({candidate.work_id})")
        else:
            print(f"Candidate {candidate.work_id} already exists in SQLite")
    
    # Migrate Templates
    print("\nMigrating Templates...")
    neon_templates = Template.objects.using('neon').all()
    templates_count = neon_templates.count()
    print(f"Found {templates_count} templates in Neon database")
    
    for template in neon_templates:
        # Check if template already exists in SQLite
        if not Template.objects.using('default').filter(name=template.name).exists():
            # Create new template in SQLite
            sqlite_template = Template(
                name=template.name,
                role=template.role,
                file=template.file,
                is_active=template.is_active,
                created_by_id=template.created_by_id,
                created_by_username=template.created_by_username,
                created_at=template.created_at
            )
            sqlite_template.save(using='default')
            print(f"Migrated template: {template.name}")
        else:
            print(f"Template {template.name} already exists in SQLite")
    
    # Migrate Offer Letters
    print("\nMigrating Offer Letters...")
    neon_offer_letters = OfferLetter.objects.using('neon').all()
    offer_letters_count = neon_offer_letters.count()
    print(f"Found {offer_letters_count} offer letters in Neon database")
    
    for offer_letter in neon_offer_letters:
        # Find the corresponding candidate in SQLite
        try:
            sqlite_candidate = Candidate.objects.using('default').get(work_id=offer_letter.candidate.work_id)
            
            # Check if offer letter already exists in SQLite
            if not OfferLetter.objects.using('default').filter(candidate_work_id=offer_letter.candidate_work_id).exists():
                # Create new offer letter in SQLite
                sqlite_offer_letter = OfferLetter(
                    candidate_id=offer_letter.candidate_id,
                    template_id=offer_letter.template_id,
                    candidate_work_id=offer_letter.candidate_work_id,
                    template_name=offer_letter.template_name,
                    generated_file=offer_letter.generated_file,
                    pdf_file=offer_letter.pdf_file,
                    sent_at=offer_letter.sent_at,
                    created_at=offer_letter.created_at
                )
                sqlite_offer_letter.save(using='default')
                print(f"Migrated offer letter for candidate: {sqlite_candidate.name}")
            else:
                print(f"Offer letter for candidate {sqlite_candidate.work_id} already exists in SQLite")
        except Candidate.DoesNotExist:
            print(f"Could not find candidate {offer_letter.candidate.work_id} in SQLite, skipping offer letter")
    
    print("\nMigration completed successfully!")

def verify_migration():
    """Verify the migration by comparing counts"""
    print("\nVerifying migration...")
    
    # Compare candidate counts
    neon_candidates = Candidate.objects.using('neon').count()
    sqlite_candidates = Candidate.objects.using('default').count()
    print(f"Candidates - Neon: {neon_candidates}, SQLite: {sqlite_candidates}")
    
    # Compare template counts
    neon_templates = Template.objects.using('neon').count()
    sqlite_templates = Template.objects.using('default').count()
    print(f"Templates - Neon: {neon_templates}, SQLite: {sqlite_templates}")
    
    # Compare offer letter counts
    neon_offer_letters = OfferLetter.objects.using('neon').count()
    sqlite_offer_letters = OfferLetter.objects.using('default').count()
    print(f"Offer Letters - Neon: {neon_offer_letters}, SQLite: {sqlite_offer_letters}")

if __name__ == '__main__':
    try:
        migrate_data()
        verify_migration()
    except Exception as e:
        print(f"Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
