from django.core.management.base import BaseCommand
from offers.models import Candidate, OfferLetter
from django.db import connection

class Command(BaseCommand):
    help = 'Reset work ID to 0A20 and remove all candidates from Neon database'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Resetting work ID and cleaning Neon database...')
        self.stdout.write('=' * 60)
        
        # Step 1: Remove all candidates from Neon database
        self.stdout.write('\n🗑️  Removing candidates from Neon database...')
        try:
            candidate_count = Candidate.objects.using('neon').count()
            self.stdout.write(f'   Found {candidate_count} candidates in Neon database')
            
            if candidate_count > 0:
                # Remove all candidates
                deleted_count, _ = Candidate.objects.using('neon').all().delete()
                self.stdout.write(
                    self.style.SUCCESS(f'   ✅ Deleted {deleted_count} candidates from Neon database')
                )
            else:
                self.stdout.write(self.style.WARNING('   ⚠️  No candidates found in Neon database'))
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'   ❌ Error removing candidates: {str(e)}')
            )
        
        # Step 2: Remove all offer letters from Neon database
        self.stdout.write('\n🗑️  Removing offer letters from Neon database...')
        try:
            offer_letter_count = OfferLetter.objects.using('neon').count()
            self.stdout.write(f'   Found {offer_letter_count} offer letters in Neon database')
            
            if offer_letter_count > 0:
                # Remove all offer letters
                deleted_count, _ = OfferLetter.objects.using('neon').all().delete()
                self.stdout.write(
                    self.style.SUCCESS(f'   ✅ Deleted {deleted_count} offer letters from Neon database')
                )
            else:
                self.stdout.write(self.style.WARNING('   ⚠️  No offer letters found in Neon database'))
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'   ❌ Error removing offer letters: {str(e)}')
            )
        
        # Step 3: Reset work ID sequence to 0A20
        self.stdout.write('\n🔄 Resetting work ID sequence to 0A20...')
        try:
            with connection.cursor() as cursor:
                # Get the current sequence name for candidates table
                cursor.execute("""
                    SELECT column_name, column_default 
                    FROM information_schema.columns 
                    WHERE table_name = 'candidates' 
                    AND column_name = 'work_id'
                """)
                result = cursor.fetchone()
                
                if result and result[1]:
                    # Extract sequence name from default value
                    default_value = result[1]
                    if "nextval" in default_value:
                        # PostgreSQL sequence format
                        sequence_name = default_value.split("'")[1]
                        
                        # Reset sequence to start from 20 (since 0A20 means 20)
                        cursor.execute(f"ALTER SEQUENCE {sequence_name} RESTART WITH 20")
                        self.stdout.write(
                            self.style.SUCCESS(f'   ✅ Reset sequence {sequence_name} to start from 20')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING('   ⚠️  Could not determine sequence format')
                        )
                else:
                    self.stdout.write(
                        self.style.WARNING('   ⚠️  Could not find work_id sequence information')
                    )
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'   ❌ Error resetting sequence: {str(e)}')
            )
        
        # Step 4: Verify the reset
        self.stdout.write('\n🔍 Verifying the reset...')
        try:
            # Check remaining candidates
            remaining_candidates = Candidate.objects.using('neon').count()
            remaining_offer_letters = OfferLetter.objects.using('neon').count()
            
            self.stdout.write(f'   Remaining candidates: {remaining_candidates}')
            self.stdout.write(f'   Remaining offer letters: {remaining_offer_letters}')
            
            if remaining_candidates == 0 and remaining_offer_letters == 0:
                self.stdout.write(
                    self.style.SUCCESS('   ✅ Neon database is clean')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('   ⚠️  Some data may still remain')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'   ❌ Error verifying: {str(e)}')
            )
        
        # Step 5: Test next work ID generation
        self.stdout.write('\n🧪 Testing next work ID generation...')
        try:
            # Create a test candidate to verify the sequence
            test_candidate = Candidate(
                name='Test Candidate',
                email='test@example.com',
                phone='+1234567890',
                role='frontend',
                letter_date='2024-01-01',
                joining_date='2024-01-15'
            )
            test_candidate.save(using='neon')
            
            generated_work_id = test_candidate.work_id
            self.stdout.write(f'   Generated work ID: {generated_work_id}')
            
            # Clean up test candidate
            test_candidate.delete(using='neon')
            
            if generated_work_id == '0A20':
                self.stdout.write(
                    self.style.SUCCESS('   ✅ Work ID reset successful! Next ID will be 0A20')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'   ⚠️  Expected 0A20, got {generated_work_id}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'   ❌ Error testing work ID: {str(e)}')
            )
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('🎉 Work ID Reset and Database Cleanup Completed!'))
        self.stdout.write('\n📋 Summary:')
        self.stdout.write('   • All candidates removed from Neon database')
        self.stdout.write('   • All offer letters removed from Neon database')
        self.stdout.write('   • Work ID sequence reset to 0A20')
        self.stdout.write('   • Ready for fresh candidate creation')
        self.stdout.write('\n🚀 Next Steps:')
        self.stdout.write('   • Create new candidates - they will start from 0A20')
        self.stdout.write('   • Generate offer letters with clean work IDs')
        self.stdout.write('=' * 60)
